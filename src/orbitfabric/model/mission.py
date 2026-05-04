from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Criticality = Literal["low", "medium", "high", "critical"]
Severity = Literal["info", "warning", "error", "critical"]
DownlinkPriority = Literal["low", "medium", "high", "critical"]
PersistencePolicy = Literal["none", "store", "downlink_only", "store_and_downlink"]
CommandRisk = Literal["low", "medium", "high", "critical"]

TelemetryType = Literal[
    "bool",
    "uint8",
    "uint16",
    "uint32",
    "int8",
    "int16",
    "int32",
    "float32",
    "float64",
    "enum",
    "string",
]

PacketType = Literal["json", "binary_compact", "ccsds_like"]
PayloadProfile = Literal["iod", "mission_specific"]
DataProductProducerType = Literal["payload", "subsystem"]
DataProductType = Literal[
    "histogram",
    "image",
    "sample_batch",
    "capture_window",
    "diagnostic_dump",
    "compressed_product",
    "generic",
]
StorageClass = Literal["science", "diagnostic", "housekeeping", "engineering"]
OverflowPolicy = Literal["drop_oldest", "drop_newest", "reject_new", "overwrite", "none"]
DownlinkIntentPolicy = Literal[
    "none",
    "next_available_contact",
    "priority_based",
    "deferred",
    "manual",
]


ContactLinkDirection = Literal["downlink"]
DownlinkFlowQueuePolicy = Literal[
    "priority_then_age",
    "oldest_first",
    "manual_selection",
    "critical_first",
]


class StrictModel(BaseModel):
    """Base Pydantic model used by OrbitFabric Mission Model objects."""

    model_config = ConfigDict(extra="forbid")


class Spacecraft(StrictModel):
    id: str
    name: str
    spacecraft_class: str = Field(alias="class")
    form_factor: str | None = None
    mission_type: str | None = None
    model_version: str


class Subsystem(StrictModel):
    id: str
    name: str
    type: str
    criticality: Criticality
    description: str | None = None


class Mode(StrictModel):
    description: str
    initial: bool = False


class ModeTransition(StrictModel):
    from_mode: str = Field(alias="from")
    to: str
    reason: str
    description: str | None = None


class TelemetryLimits(StrictModel):
    warning_low: float | None = None
    critical_low: float | None = None
    warning_high: float | None = None
    critical_high: float | None = None


class QualityPolicy(StrictModel):
    required: bool = False
    default: str | None = None


class TelemetryItem(StrictModel):
    id: str
    name: str
    type: TelemetryType
    unit: str
    source: str
    sampling: str
    criticality: Criticality
    persistence: PersistencePolicy
    downlink_priority: DownlinkPriority
    limits: TelemetryLimits | None = None
    enum: list[str] | None = None
    quality: QualityPolicy | None = None
    description: str | None = None


class CommandArgument(StrictModel):
    name: str
    type: TelemetryType
    min: float | int | None = None
    max: float | int | None = None
    enum: list[str] | None = None
    default: Any | None = None
    description: str | None = None


class Command(StrictModel):
    id: str
    target: str
    description: str
    arguments: list[CommandArgument]
    allowed_modes: list[str]
    preconditions: list[Any] | dict[str, Any] | None = None
    requires_ack: bool
    timeout_ms: int | None = None
    risk: CommandRisk
    emits: list[str] = Field(default_factory=list)
    expected_effects: dict[str, Any] = Field(default_factory=dict)


class Event(StrictModel):
    id: str
    source: str
    severity: Severity
    description: str
    downlink_priority: DownlinkPriority | None = None
    persistence: PersistencePolicy | None = None


class FaultCondition(StrictModel):
    telemetry: str | None = None
    event: str | None = None
    operator: str | None = None
    value: Any | None = None
    debounce_samples: int | None = None
    occurrences: int | None = None
    window_s: int | None = None


class FaultRecovery(StrictModel):
    mode_transition: str | None = None
    auto_commands: list[str] = Field(default_factory=list)


class Fault(StrictModel):
    id: str
    source: str
    severity: Severity
    description: str
    condition: FaultCondition
    emits: list[str]
    recovery: FaultRecovery | None = None


class Packet(StrictModel):
    id: str
    name: str
    type: PacketType
    max_payload_bytes: int
    period: str | None = None
    telemetry: list[str]
    description: str | None = None


class PayloadLifecycle(StrictModel):
    initial_state: str
    states: list[str]


class PayloadTelemetryRefs(StrictModel):
    produced: list[str] = Field(default_factory=list)


class PayloadCommandRefs(StrictModel):
    accepted: list[str] = Field(default_factory=list)


class PayloadEventRefs(StrictModel):
    generated: list[str] = Field(default_factory=list)


class PayloadFaultRefs(StrictModel):
    possible: list[str] = Field(default_factory=list)


class PayloadContract(StrictModel):
    id: str
    subsystem: str
    profile: PayloadProfile
    lifecycle: PayloadLifecycle
    telemetry: PayloadTelemetryRefs = Field(default_factory=PayloadTelemetryRefs)
    commands: PayloadCommandRefs = Field(default_factory=PayloadCommandRefs)
    events: PayloadEventRefs = Field(default_factory=PayloadEventRefs)
    faults: PayloadFaultRefs = Field(default_factory=PayloadFaultRefs)
    description: str | None = None


class DataProductStorageIntent(StrictModel):
    storage_class: StorageClass = Field(alias="class")
    retention: str | None = None
    overflow_policy: OverflowPolicy | None = None


class DataProductDownlinkIntent(StrictModel):
    policy: DownlinkIntentPolicy | None = None


class DataProductContract(StrictModel):
    id: str
    producer: str
    producer_type: DataProductProducerType
    type: DataProductType
    estimated_size_bytes: int = Field(gt=0)
    priority: DownlinkPriority
    payload: str | None = None
    storage: DataProductStorageIntent | None = None
    downlink: DataProductDownlinkIntent | None = None
    description: str | None = None


class ContactProfile(StrictModel):
    id: str
    target: str
    description: str | None = None


class LinkProfile(StrictModel):
    id: str
    direction: ContactLinkDirection
    assumed_rate_bps: int | None = Field(default=None, gt=0)
    description: str | None = None


class ContactWindow(StrictModel):
    id: str
    contact_profile: str
    link_profile: str
    start: str
    duration_seconds: int = Field(gt=0)
    assumed_capacity_bytes: int | None = Field(default=None, gt=0)
    description: str | None = None


class DownlinkFlowContract(StrictModel):
    id: str
    contact_profile: str
    link_profile: str
    queue_policy: DownlinkFlowQueuePolicy
    eligible_data_products: list[str] = Field(default_factory=list)
    description: str | None = None


class ContactContracts(StrictModel):
    contact_profiles: list[ContactProfile] = Field(default_factory=list)
    link_profiles: list[LinkProfile] = Field(default_factory=list)
    contact_windows: list[ContactWindow] = Field(default_factory=list)
    downlink_flows: list[DownlinkFlowContract] = Field(default_factory=list)


class AllowedValues(StrictModel):
    allowed_values: list[str]


class Policies(StrictModel):
    persistence: AllowedValues
    downlink_priority: AllowedValues
    command_risk: AllowedValues
    event_severity: AllowedValues | None = None
    telemetry_criticality: AllowedValues | None = None


class MissionModel(StrictModel):
    spacecraft: Spacecraft
    subsystems: list[Subsystem]
    modes: dict[str, Mode]
    mode_transitions: list[ModeTransition]
    telemetry: list[TelemetryItem]
    commands: list[Command]
    events: list[Event]
    faults: list[Fault]
    packets: list[Packet]
    policies: Policies
    payloads: list[PayloadContract] = Field(default_factory=list)
    data_products: list[DataProductContract] = Field(default_factory=list)
    contacts: ContactContracts = Field(default_factory=ContactContracts)

    @property
    def subsystem_ids(self) -> set[str]:
        return {item.id for item in self.subsystems}

    @property
    def telemetry_ids(self) -> set[str]:
        return {item.id for item in self.telemetry}

    @property
    def command_ids(self) -> set[str]:
        return {item.id for item in self.commands}

    @property
    def event_ids(self) -> set[str]:
        return {item.id for item in self.events}

    @property
    def fault_ids(self) -> set[str]:
        return {item.id for item in self.faults}

    @property
    def packet_ids(self) -> set[str]:
        return {item.id for item in self.packets}

    @property
    def payload_ids(self) -> set[str]:
        return {item.id for item in self.payloads}

    @property
    def data_product_ids(self) -> set[str]:
        return {item.id for item in self.data_products}

    @property
    def contact_profile_ids(self) -> set[str]:
        return {item.id for item in self.contacts.contact_profiles}

    @property
    def link_profile_ids(self) -> set[str]:
        return {item.id for item in self.contacts.link_profiles}

    @property
    def contact_window_ids(self) -> set[str]:
        return {item.id for item in self.contacts.contact_windows}

    @property
    def downlink_flow_ids(self) -> set[str]:
        return {item.id for item in self.contacts.downlink_flows}

    @property
    def mode_ids(self) -> set[str]:
        return set(self.modes.keys())