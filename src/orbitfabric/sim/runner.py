from __future__ import annotations

from typing import Any

from orbitfabric.model.mission import (
    DataProductContract,
    DataProductDownlinkIntent,
    DataProductStorageIntent,
    MissionModel,
)
from orbitfabric.model.scenario import LoadedScenario, ScenarioStep
from orbitfabric.sim.command_router import CommandDispatchResult, CommandRouter
from orbitfabric.sim.event_bus import EventBus
from orbitfabric.sim.fault_monitor import FaultMonitor, FaultTrigger
from orbitfabric.sim.mode_manager import ModeManager
from orbitfabric.sim.state import (
    SimDataFlowEvidenceRecord,
    SimulationResult,
    SimulationState,
)
from orbitfabric.sim.telemetry_registry import TelemetryRegistry


class ScenarioRunner:
    """Runs a loaded scenario against its Mission Model."""

    def run(self, loaded: LoadedScenario) -> SimulationResult:
        scenario = loaded.scenario
        mission = loaded.mission_model

        state = SimulationState(
            current_time=0,
            current_mode=scenario.initial_state.mode,
            telemetry=dict(scenario.initial_state.telemetry),
            payload_lifecycle={
                payload.id: payload.lifecycle.initial_state
                for payload in mission.payloads
            },
        )

        telemetry = TelemetryRegistry(state)
        event_bus = EventBus(mission, state)
        mode_manager = ModeManager(state, telemetry)
        command_router = CommandRouter(mission, state)
        fault_monitor = FaultMonitor(mission, telemetry)

        mode_manager.initialize(t=0)
        self._initialize_payload_lifecycle(state)

        for step in scenario.steps:
            state.current_time = step.t
            self._execute_step(
                step=step,
                mission=mission,
                state=state,
                telemetry=telemetry,
                event_bus=event_bus,
                mode_manager=mode_manager,
                command_router=command_router,
                fault_monitor=fault_monitor,
            )

        if state.passed:
            state.log(state.current_time, "SCENARIO PASSED")
        else:
            state.log(state.current_time, "SCENARIO FAILED")

        return SimulationResult(
            scenario_id=scenario.scenario.id,
            mission_id=mission.spacecraft.id,
            state=state,
        )

    def _initialize_payload_lifecycle(self, state: SimulationState) -> None:
        for payload_id, lifecycle_state in sorted(state.payload_lifecycle.items()):
            state.log(0, f"PAYLOAD {payload_id} LIFECYCLE={lifecycle_state}")

    def _execute_step(
        self,
        step: ScenarioStep,
        mission: MissionModel,
        state: SimulationState,
        telemetry: TelemetryRegistry,
        event_bus: EventBus,
        mode_manager: ModeManager,
        command_router: CommandRouter,
        fault_monitor: FaultMonitor,
    ) -> None:
        if step.command is not None:
            result = command_router.dispatch(
                command_id=step.command,
                args=step.args,
                dispatch="GROUND",
                t=step.t,
            )
            self._apply_command_effects(
                result=result,
                mission=mission,
                t=step.t,
                state=state,
                telemetry=telemetry,
                event_bus=event_bus,
                mode_manager=mode_manager,
            )
            self._check_command_status_expectation(step, result, state)

        if step.inject is not None:
            telemetry.inject(step.inject.telemetry, step.inject.value, step.t)
            self._apply_fault_triggers(
                triggers=fault_monitor.evaluate(),
                mission=mission,
                t=step.t,
                state=state,
                telemetry=telemetry,
                event_bus=event_bus,
                mode_manager=mode_manager,
                command_router=command_router,
            )

        self._check_expectations(
            step=step,
            state=state,
            telemetry=telemetry,
            event_bus=event_bus,
            mode_manager=mode_manager,
            command_router=command_router,
        )

    def _apply_command_effects(
        self,
        result: CommandDispatchResult,
        mission: MissionModel,
        t: float,
        state: SimulationState,
        telemetry: TelemetryRegistry,
        event_bus: EventBus,
        mode_manager: ModeManager,
    ) -> None:
        if result.command is None:
            return

        if result.status not in {"ACCEPTED", "AUTO_DISPATCHED"}:
            return

        command = result.command

        for event_id in command.emits:
            event_bus.emit(event_id, t)

        expected_effects = command.expected_effects
        self._apply_payload_lifecycle_effects(expected_effects, state, t)
        self._record_data_flow_evidence(expected_effects, command.id, mission, state, t)

        telemetry_effects = expected_effects.get("telemetry", {})
        for telemetry_id, value in telemetry_effects.items():
            telemetry.set(telemetry_id, value, t, log=True)

        mode_transition = expected_effects.get("mode_transition")
        if isinstance(mode_transition, dict):
            target_mode = mode_transition.get("to")
            if target_mode is not None:
                reason = command.emits[0] if command.emits else command.id
                mode_manager.transition_to(target_mode, reason, t)

    def _apply_payload_lifecycle_effects(
        self,
        expected_effects: dict[str, Any],
        state: SimulationState,
        t: float,
    ) -> None:
        lifecycle_effect = expected_effects.get("payload_lifecycle")
        if not isinstance(lifecycle_effect, dict):
            return

        payload_id = lifecycle_effect.get("payload")
        lifecycle_state = lifecycle_effect.get("state")

        if not isinstance(payload_id, str) or not isinstance(lifecycle_state, str):
            return

        state.payload_lifecycle[payload_id] = lifecycle_state
        state.log(t, f"PAYLOAD {payload_id} LIFECYCLE={lifecycle_state}")

    def _record_data_flow_evidence(
        self,
        expected_effects: dict[str, Any],
        command_id: str,
        mission: MissionModel,
        state: SimulationState,
        t: float,
    ) -> None:
        data_product_ids = expected_effects.get("data_products")
        if not isinstance(data_product_ids, list):
            return

        data_products = {data_product.id: data_product for data_product in mission.data_products}
        for data_product_id in data_product_ids:
            if not isinstance(data_product_id, str):
                continue

            data_product = data_products.get(data_product_id)
            if data_product is None:
                continue

            evidence = _build_data_flow_evidence(
                data_product=data_product,
                command_id=command_id,
                mission=mission,
                t=t,
            )
            state.data_flow_evidence.append(evidence)
            state.log(t, f"DATA_PRODUCT {data_product_id} CONTRACT_EVIDENCE_RECORDED")

    def _apply_fault_triggers(
        self,
        triggers: list[FaultTrigger],
        mission: MissionModel,
        t: float,
        state: SimulationState,
        telemetry: TelemetryRegistry,
        event_bus: EventBus,
        mode_manager: ModeManager,
        command_router: CommandRouter,
    ) -> None:
        for trigger in triggers:
            for event_id in trigger.emitted_events:
                event_bus.emit(event_id, t)

            if trigger.mode_transition is not None:
                mode_manager.transition_to(trigger.mode_transition, trigger.fault_id, t)

            for command_id in trigger.auto_commands:
                result = command_router.dispatch(
                    command_id=command_id,
                    args={},
                    dispatch="AUTO",
                    t=t,
                )
                self._apply_command_effects(
                    result=result,
                    mission=mission,
                    t=t,
                    state=state,
                    telemetry=telemetry,
                    event_bus=event_bus,
                    mode_manager=mode_manager,
                )

    def _check_command_status_expectation(
        self,
        step: ScenarioStep,
        result: CommandDispatchResult,
        state: SimulationState,
    ) -> None:
        if step.expect is None:
            return

        expected_status = step.expect.get("command_status")
        if expected_status is None:
            return

        if result.status != expected_status:
            state.fail_expectation(
                step.t,
                f"expected command status {expected_status} but got {result.status}",
            )

    def _check_expectations(
        self,
        step: ScenarioStep,
        state: SimulationState,
        telemetry: TelemetryRegistry,
        event_bus: EventBus,
        mode_manager: ModeManager,
        command_router: CommandRouter,
    ) -> None:
        if step.expect_event is not None and not event_bus.has_event(step.expect_event):
            state.fail_expectation(step.t, f"missing event {step.expect_event}")

        if step.expect_mode is not None and mode_manager.current_mode != step.expect_mode:
            state.fail_expectation(
                step.t,
                f"expected mode {step.expect_mode} but got {mode_manager.current_mode}",
            )

        if step.expect_command is not None:
            expected_dispatch = step.expect_command.dispatch
            if not command_router.has_command(step.expect_command.id, expected_dispatch):
                state.fail_expectation(
                    step.t,
                    "missing command "
                    f"{step.expect_command.id} with dispatch {expected_dispatch}",
                )

        if step.expect_telemetry is not None:
            self._check_telemetry_expectations(step, telemetry, state)

        if step.expect is not None:
            self._check_payload_lifecycle_expectation(step, state)
            self._check_data_flow_expectation(step, state)
            self._check_scenario_status_expectation(step, state)

    def _check_telemetry_expectations(
        self,
        step: ScenarioStep,
        telemetry: TelemetryRegistry,
        state: SimulationState,
    ) -> None:
        if step.expect_telemetry is None:
            return

        for telemetry_id, expected_value in step.expect_telemetry.items():
            actual_value = telemetry.get(telemetry_id)
            if actual_value != expected_value:
                state.fail_expectation(
                    step.t,
                    f"expected telemetry {telemetry_id}={_format_value(expected_value)} "
                    f"but got {_format_value(actual_value)}",
                )
            else:
                state.log(
                    step.t,
                    f"TELEMETRY {telemetry_id}={_format_value(actual_value)}",
                )

    def _check_payload_lifecycle_expectation(
        self,
        step: ScenarioStep,
        state: SimulationState,
    ) -> None:
        if step.expect is None:
            return

        expected_lifecycle = step.expect.get("payload_lifecycle")
        if not isinstance(expected_lifecycle, dict):
            return

        payload_id = expected_lifecycle.get("payload")
        expected_state = expected_lifecycle.get("state")

        if not isinstance(payload_id, str) or not isinstance(expected_state, str):
            state.fail_expectation(step.t, "invalid payload lifecycle expectation")
            return

        actual_state = state.payload_lifecycle.get(payload_id)
        if actual_state != expected_state:
            state.fail_expectation(
                step.t,
                f"expected payload {payload_id} lifecycle {expected_state} "
                f"but got {actual_state}",
            )
        else:
            state.log(step.t, f"PAYLOAD {payload_id} LIFECYCLE={actual_state}")

    def _check_data_flow_expectation(
        self,
        step: ScenarioStep,
        state: SimulationState,
    ) -> None:
        if step.expect is None:
            return

        expected_data_flow = step.expect.get("data_flow")
        if not isinstance(expected_data_flow, dict):
            return

        data_product_id = expected_data_flow.get("data_product")
        if not isinstance(data_product_id, str):
            state.fail_expectation(step.t, "invalid data flow expectation")
            return

        evidence = _find_data_flow_evidence(state, data_product_id)
        if evidence is None:
            state.fail_expectation(
                step.t,
                f"missing data flow evidence for {data_product_id}",
            )
            return

        mismatches = _data_flow_expectation_mismatches(expected_data_flow, evidence)
        if mismatches:
            state.fail_expectation(step.t, "; ".join(mismatches))
        else:
            state.log(step.t, f"DATA_FLOW {data_product_id} EXPECTATION_MET")

    def _check_scenario_status_expectation(
        self,
        step: ScenarioStep,
        state: SimulationState,
    ) -> None:
        if step.expect is None:
            return

        expected_status = step.expect.get("scenario_status")
        if expected_status is None:
            return

        actual_status = "PASSED" if state.passed else "FAILED"
        if actual_status != expected_status:
            state.fail_expectation(
                step.t,
                f"expected scenario status {expected_status} but got {actual_status}",
            )


def _build_data_flow_evidence(
    data_product: DataProductContract,
    command_id: str,
    mission: MissionModel,
    t: float,
) -> SimDataFlowEvidenceRecord:
    eligible_flows = [
        flow.id
        for flow in mission.contacts.downlink_flows
        if data_product.id in flow.eligible_data_products
    ]
    contact_windows = _contact_windows_for_flows(eligible_flows, mission)

    return SimDataFlowEvidenceRecord(
        t=t,
        data_product_id=data_product.id,
        producer=data_product.producer,
        producer_type=data_product.producer_type,
        command_id=command_id,
        storage_intent=_storage_intent_to_dict(data_product.storage),
        downlink_intent=_downlink_intent_to_dict(data_product.downlink),
        eligible_downlink_flows=eligible_flows,
        contact_windows=contact_windows,
    )


def _contact_windows_for_flows(
    flow_ids: list[str],
    mission: MissionModel,
) -> list[str]:
    flows = [flow for flow in mission.contacts.downlink_flows if flow.id in flow_ids]
    windows: list[str] = []

    for flow in flows:
        for window in mission.contacts.contact_windows:
            if window.contact_profile != flow.contact_profile:
                continue
            if window.link_profile != flow.link_profile:
                continue
            windows.append(window.id)

    return sorted(set(windows))


def _storage_intent_to_dict(
    storage: DataProductStorageIntent | None,
) -> dict[str, Any]:
    if storage is None:
        return {"declared": False}

    return {
        "declared": True,
        "class": storage.storage_class,
        "retention": storage.retention,
        "overflow_policy": storage.overflow_policy,
    }


def _downlink_intent_to_dict(
    downlink: DataProductDownlinkIntent | None,
) -> dict[str, Any]:
    if downlink is None:
        return {"declared": False}

    return {
        "declared": downlink.policy is not None,
        "policy": downlink.policy,
    }


def _find_data_flow_evidence(
    state: SimulationState,
    data_product_id: str,
) -> SimDataFlowEvidenceRecord | None:
    for evidence in reversed(state.data_flow_evidence):
        if evidence.data_product_id == data_product_id:
            return evidence

    return None


def _data_flow_expectation_mismatches(
    expected: dict[str, Any],
    evidence: SimDataFlowEvidenceRecord,
) -> list[str]:
    mismatches: list[str] = []

    triggered_by_command = expected.get("triggered_by_command")
    if triggered_by_command is not None and triggered_by_command != evidence.command_id:
        mismatches.append(
            f"expected data flow command {triggered_by_command} "
            f"but got {evidence.command_id}"
        )

    storage_declared = expected.get("storage_intent_declared")
    if storage_declared is not None:
        actual = evidence.storage_intent.get("declared")
        if storage_declared != actual:
            mismatches.append(
                f"expected storage_intent_declared={storage_declared} but got {actual}"
            )

    downlink_declared = expected.get("downlink_intent_declared")
    if downlink_declared is not None:
        actual = evidence.downlink_intent.get("declared")
        if downlink_declared != actual:
            mismatches.append(
                f"expected downlink_intent_declared={downlink_declared} but got {actual}"
            )

    eligible_downlink_flow = expected.get("eligible_downlink_flow")
    if eligible_downlink_flow is not None:
        if eligible_downlink_flow not in evidence.eligible_downlink_flows:
            mismatches.append(
                f"expected eligible downlink flow {eligible_downlink_flow}"
            )

    contact_window = expected.get("contact_window")
    if contact_window is not None and contact_window not in evidence.contact_windows:
        mismatches.append(f"expected contact window {contact_window}")

    return mismatches


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)