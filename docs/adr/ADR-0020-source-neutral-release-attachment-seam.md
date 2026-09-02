# ADR-0020 - Source-Neutral Release Attachment Seam

Status: **Accepted candidate Core architecture**  
Date: **2026-09-02**

## Context

OrbitFabric Core already owns:

```text
Adapter Project Lock
    exact project desired adapter state

ResolvedAdapterRelease
    exact resolved release handoff

AdapterManager.install_resolved(...)
    shared post-resolution lifecycle transaction
```

The first install-from-lock lane was intentionally explicit-source only. Its convenience path resolved local Release Descriptor and artifact files before performing provider-neutral lock verification and installation.

The next architecture question was whether remote release material required a registry subsystem or provider-specific lifecycle path.

A private F Prime control resolved exact Release Descriptor and wheel assets from a temporary private GitHub Release, verified downloaded bytes and then installed the already-resolved release through the same lock and Adapter Manager boundaries.

## Decision

Core retains `ResolvedAdapterRelease` as the provider-neutral source-to-lifecycle handoff.

`ProjectLockInstallService` exposes a candidate resolved-release entry point that performs the existing provider-neutral portion of install-from-lock:

```text
ResolvedAdapterRelease
    -> exact Project Lock identity verification
    -> locked Installation Backend verification
    -> AdapterManager.install_resolved(...)
    -> post-install Project Lock re-check
```

The existing explicit-source path remains a convenience wrapper and preserves its CLI behavior.

## MATCH ordering

The explicit-source wrapper checks current project state before invoking source resolution.

Therefore:

```text
MATCH
    -> NOOP
    -> no additional source resolution
```

A remote source orchestrator must preserve the same ordering by checking project state before performing remote resolution.

## Provider neutrality

This ADR does not introduce:

```text
GitHubReleaseSource
public source-provider protocol
public source configuration schema
public registry
remote source CLI
```

Provider-specific resolution may remain outside Core while producing the generic `ResolvedAdapterRelease` handoff.

GitHub Release was used only as a falsification/control provider.

## Project Lock boundary

Remote transport locators do not become Adapter Project Lock identity.

The lock continues to bind exact generic identity:

```text
Source Coordinate
Release Version
Release Descriptor SHA-256
Artifact ID
Artifact SHA-256
Installation Backend ID
```

Repository URLs, release URLs, asset URLs and download paths remain source configuration or transport metadata.

## Temporary source material

`ResolvedAdapterRelease` currently references local materialized descriptor and artifact paths during installation.

A remote resolver may therefore use a temporary workspace.

After installation completes, normal installed verification and execution depend on Core-managed installed state rather than the original source workspace or network.

The F Prime remote control removed the downloaded source workspace and retained successful installed adapter verification.

## Trust separation

Remote resolution and exact byte verification remain distinct from publisher trust and release acceptance.

The following implications remain invalid:

```text
remote download success != trusted release
asset digest match != publisher authenticity
private repository != OrbitFabric official status
exact historical bytes != current operational acceptance
```

Acceptance continues through the existing Adapter Manager policy boundary.

## Compatibility

This is an additive Adapter Manager capability.

It does not change:

```text
Mission Model semantics
Adapter Project Lock 0.1-candidate schema
Adapter Release Descriptor 0.1-candidate schema
Installed Adapter Inventory identity
Integration Package Manifest
orbitfabric.adapter_cli.v1
Integration Result
existing explicit-source CLI syntax
```

## Deferred

```text
built-in remote Release Source providers
public Release Source provider interface
public source configuration persistence
registry topology and discovery
publisher administration
project-wide reconcile
automatic update/removal
Studio lifecycle UX
```

Those require separate evidence and decisions.