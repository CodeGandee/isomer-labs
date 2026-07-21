# isomer-misc-tool-packs-skill Specification

## Purpose
Define the manually invoked misc skill that resolves named tool packs into installable dependency contracts.
## Requirements
### Requirement: Misc Tool Packs Skill Resolves Named Toolsets
The core public pack SHALL preserve logical capability `isomer-misc-tool-packs` as protected shared member `tool-packs` for resolving named dependency bundles.

#### Scenario: Protected tool-packs bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-tool-packs/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-misc-tool-packs`

#### Scenario: User manually asks to install a named toolset
- **WHEN** a user explicitly invokes `isomer-misc-tool-packs` or directly asks to install or prepare a toolset such as `paper-writing`, `paper-figures-python`, `paper2ppt`, `cuda-build`, or `torch-gpu`
- **THEN** the skill resolves the request to one canonical pack name
- **AND** it reports the aliases that matched when aliases were used
- **AND** it returns a dependency contract for the canonical pack

#### Scenario: Named toolset is requested
- **WHEN** a user or owning workflow asks for one defined tool pack
- **THEN** the public parent or internal route invokes `isomer-op-entrypoint->tool-packs`
- **AND** the protected capability returns the existing dependency intent without applying package mutation itself

#### Scenario: Ambiguous toolset name blocks resolution
- **WHEN** a user-provided toolset name can plausibly match more than one canonical pack
- **THEN** the skill reports an ambiguity blocker
- **AND** it lists the candidate canonical pack names without choosing one silently

#### Scenario: Unknown toolset remains bounded
- **WHEN** a named toolset is absent from the tool-pack registry
- **THEN** the protected capability reports it as unknown and does not fabricate dependencies

#### Scenario: Unknown toolset name blocks resolution
- **WHEN** a user-provided toolset name does not match any canonical pack or alias
- **THEN** the skill reports an unknown-toolset blocker
- **AND** it lists the available canonical pack names

### Requirement: Tool Pack Contracts Expose Installable Dependency Intent
The tool-pack skill SHALL return pack contracts that downstream setup skills can convert into concrete environment mutation and verification steps.

#### Scenario: Pack contract is returned
- **WHEN** the skill resolves a canonical pack
- **THEN** the result includes purpose, included packs when any, required tools, optional tools, dependency kind, package-source hints, host or external-tool expectations, verification checks, blockers, and owning helper-skill routes
- **AND** the result distinguishes required tools from optional or fallback tools

#### Scenario: CLI tools declare user-level install preference
- **WHEN** a pack contract includes a command-line tool that is distributed as a Python package
- **THEN** the contract records `uv tool install` as the preferred install route when `uv` is available and PyPI has the package
- **AND** it records `pixi global install` as the fallback route when the uv tool path is unavailable, unsuitable, or does not expose the required command
- **AND** it does not classify that CLI tool as a Topic Workspace Python library merely because it is distributed on PyPI

#### Scenario: Python libraries target topic workspace Pixi env
- **WHEN** a pack contract includes an importable Python package or library needed by the topic runnable target
- **THEN** the contract records the selected Topic Workspace Pixi environment as the install target
- **AND** it does not route that library through `uv tool install` or `pixi global install`

#### Scenario: Pack contract preserves setup ownership
- **WHEN** the skill returns a pack contract
- **THEN** it states that actual Pixi mutation, package-source resolution, environment enclosure, and readiness verification belong to `isomer-srv-topic-env-setup`
- **AND** it does not instruct the agent to mutate a Topic Workspace environment directly from the misc tool-pack skill

#### Scenario: Helper-skill routes are referenced
- **WHEN** a pack involves package-source, NVIDIA, PyTorch, or resource-risk concerns
- **THEN** the contract names the appropriate existing helper skill route
- **AND** package-source concerns route to `isomer-srv-resolve-pkg-repo`
- **AND** NVIDIA/CUDA environment concerns route to `isomer-misc-nvidia-tools`
- **AND** PyTorch variant concerns route to `isomer-misc-pkg-specifics`
- **AND** heavy or unknown-risk setup work routes to `isomer-misc-bounded-run-tips`

### Requirement: Paper Writing Pack Is Composite
The `paper-writing` pack SHALL include manuscript authoring and Python figure-generation tools by default.

#### Scenario: Paper writing includes Python figures
- **WHEN** the skill resolves `paper-writing`
- **THEN** the returned contract includes a manuscript-build component
- **AND** it includes a citation-bibliography component
- **AND** it includes the `paper-figures-python` pack by default

#### Scenario: Paper figures Python remains independently installable
- **WHEN** the user asks for `paper-figures-python`
- **THEN** the skill returns only the Python figure-generation pack contract
- **AND** it does not include manuscript-build tools unless the user also requested `paper-writing`

#### Scenario: Paper figures R remains opt-in
- **WHEN** the skill resolves `paper-writing`
- **THEN** it does not include `paper-figures-r` by default
- **AND** it reports `paper-figures-r` as an optional separate pack when R figure generation is desired

### Requirement: Initial Tool Packs Are Defined
The tool-pack skill SHALL define an initial catalog for the recurring Isomer setup tool groups.

#### Scenario: Initial pack catalog is inspected
- **WHEN** the tool-pack reference is inspected
- **THEN** it defines canonical packs for `paper-writing`, `paper-figures-python`, `paper-figures-r`, `paper2ppt`, `paper-citation`, `cuda-build`, `torch-gpu`, and `topic-python-starter`
- **AND** each canonical pack includes aliases, purpose, required tools, optional tools, verification checks, and route notes

#### Scenario: Paper writing build tools are represented
- **WHEN** the `paper-writing` contract is inspected
- **THEN** it names Tectonic as the preferred LaTeX build tool
- **AND** it names TeX Live fallback tools such as `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, and Biber as fallback or venue-required tools

#### Scenario: Paper figure Python tools are represented
- **WHEN** the `paper-figures-python` contract is inspected
- **THEN** it names Python figure dependencies including `matplotlib`, `numpy`, and `scipy`
- **AND** it may list common optional scientific plotting helpers such as `pandas`, `seaborn`, `statsmodels`, `scikit-image`, and `tifffile`

### Requirement: Tool Pack Skill Stays Independent of Research Paradigm Versions
The tool-pack skill SHALL describe task-level setup needs without depending on research-paradigm production DeepSci skill internals.

#### Scenario: Tool-pack guidance avoids research production DeepSci coupling
- **WHEN** the tool-pack skill and its active references are inspected
- **THEN** they do not require or reference `skillset/research-paradigm/deepsci/*` paths as consumers or dependencies
- **AND** they describe packs through task-level names such as paper writing, figures, decks, CUDA builds, and PyTorch GPU execution

#### Scenario: Operator skills are not made responsible for research tool packs
- **WHEN** the implementation is inspected
- **THEN** operator skills do not gain references to research-paradigm production DeepSci paper-writing skills as the source of tool-pack definitions
- **AND** setup-independent tool-pack knowledge remains in the misc skillset

### Requirement: Tool Pack Skill Is Manual-Only Initially
The protected tool-packs member SHALL remain explicitly selected and SHALL NOT trigger solely from a package or research task.

#### Scenario: User names tool packs
- **WHEN** the user invokes `$isomer-op-entrypoint use tool-packs to <task>` or explicitly asks for a named tool pack
- **THEN** the parent may select the protected capability

#### Scenario: Implicit invocation is disabled
- **WHEN** the tool-pack skill agent metadata is inspected
- **THEN** `allow_implicit_invocation` is set to `false`

#### Scenario: Package mutation is requested
- **WHEN** a user asks only to install, update, or remove packages
- **THEN** the entrypoint routes to the applicable owner workflow
- **AND** it does not infer tool-pack selection

### Requirement: Tool Packs Remain Misc Helper Interface
Tool packs SHALL remain cross-domain dependency intent rather than becoming a public pack or research-paradigm version.

#### Scenario: Public skill inventory is inspected
- **WHEN** ordinary Isomer host discovery runs
- **THEN** it does not list `isomer-misc-tool-packs`
- **AND** core help may expose `tool-packs` as an explicit public subcommand of `isomer-op-entrypoint`

#### Scenario: Tool-pack skill name remains stable
- **WHEN** the misc skillset is inspected after the namespace rename
- **THEN** the tool-pack skill remains `isomer-misc-tool-packs`
- **AND** it is not renamed to `isomer-ext-tool-packs`

#### Scenario: Tool-pack helper routes remain current
- **WHEN** the tool-pack skill returns a pack contract
- **THEN** package-source concerns route to `isomer-srv-resolve-pkg-repo`
- **AND** NVIDIA/CUDA environment concerns route to `isomer-misc-nvidia-tools`
- **AND** PyTorch variant concerns route to `isomer-misc-pkg-specifics`
- **AND** heavy or unknown-risk setup work routes to `isomer-misc-bounded-run-tips`

#### Scenario: Toolbox remains distinct
- **WHEN** guidance compares tool packs and Project-local Toolboxes
- **THEN** it keeps protected `tool-packs` dependency intent distinct from protected `toolbox` configuration management

#### Scenario: Tool-pack skill avoids DeepSci coupling
- **WHEN** the tool-pack skill and its active references are inspected
- **THEN** they do not require or reference production DeepSci skill paths as consumers or dependencies
- **AND** domain extension families may consume tool-pack contracts without making the tool-pack skill part of that extension family

