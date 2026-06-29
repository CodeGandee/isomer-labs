## ADDED Requirements

### Requirement: Package Source Resolution Is Delegated When It Becomes a Decision
The service environment setup enclosure workflow SHALL keep dependency installation Pixi-scoped while routing package repository, mirror, registry, or channel choice to the package repository resolver when source selection is uncertain or policy-relevant.

#### Scenario: Reachability uncertainty invokes package resolver guidance
- **WHEN** topic env setup must choose among official package sources, configured mirrors, private registries, or fallback channels before dependency mutation
- **THEN** the skill text names `isomer-srv-resolve-pkg-repo` as the package source resolution surface
- **AND** the topic env setup output records the selected source, source evidence, and any reachability or fallback warning rather than embedding an untraceable source decision

#### Scenario: Fixed gate or manifest source does not require extra resolution
- **WHEN** the environment gate, Pixi manifest, lockfile, or Service Request already fixes the package source and there is no reachability concern
- **THEN** topic env setup may use that fixed source without invoking package repository resolution
- **AND** it records the source as fixed by existing evidence

### Requirement: CUDA and NVIDIA Build Policy Is Routed to NVIDIA Tools
The service environment setup enclosure workflow SHALL route CUDA architecture, CUDA/C++ build environment, and NVIDIA build preference decisions to `isomer-misc-nvidia-tools` instead of expanding topic env setup into a general CUDA guide.

#### Scenario: CUDA build decisions use NVIDIA tools skill
- **WHEN** topic env setup encounters CUDA architecture targets, `TORCH_CUDA_ARCH_LIST`, `CMAKE_CUDA_ARCHITECTURES`, `nvcc` build flags, CUDA/C++ Pixi build environments, or CUDA build parallelism decisions
- **THEN** the skill text points to `isomer-misc-nvidia-tools` for those build preferences
- **AND** topic env setup records only the setup decisions needed for the selected Topic Workspace Pixi environment and derived gate

#### Scenario: NVIDIA channel choice remains auditable
- **WHEN** an NVIDIA tool or runtime package must be installed through Pixi channels
- **THEN** the final setup evidence records the selected channel and reason
- **AND** if channel reachability or mirror selection is uncertain, the package repository resolver provides the source decision before topic env setup mutates the Pixi manifest
