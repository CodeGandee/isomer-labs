## ADDED Requirements

### Requirement: Idea Views Answer Portfolio Questions Through Canonical Facets
Project Web SHALL let users inspect what Research Ideas were proposed, how far each was explored, which remain open, which were selected, and which were deferred or closed without interpreting one overloaded status label.

#### Scenario: User opens the default idea view
- **WHEN** a user opens the Idea Graph or Idea Timeline without restored portfolio state
- **THEN** Project Web applies the `current` preset and shows its active predicate and result counts
- **AND** primary ideas with unknown classification remain visible with a Needs Classification indication

#### Scenario: User views every proposed idea
- **WHEN** a user selects `All proposed`
- **THEN** Project Web shows all non-hidden canonical Research Ideas returned by the read model, including supporting and archived ideas
- **AND** it labels visibility and archive state so supporting material is not mistaken for a Primary Idea

#### Scenario: User views open ideas only
- **WHEN** a user selects `Open for exploration`
- **THEN** Project Web shows active ideas whose decision state is `open`, `shortlisted`, or `selected`
- **AND** it excludes deferred, closed, and unknown-decision ideas from that explicit open set

#### Scenario: User filters by exploration progress
- **WHEN** a user selects `Unexplored`, `Exploring`, or `Explored`
- **THEN** the graph or timeline filters by canonical exploration state
- **AND** selection outcome and evidence assessment remain available as separate labels and filters

#### Scenario: User filters by decision disposition
- **WHEN** a user selects `Selected`, `Deferred`, or `Closed`
- **THEN** the graph or timeline filters by canonical decision state
- **AND** exploration and evidence state remain visible independently

#### Scenario: User views ambiguous legacy ideas
- **WHEN** a user selects `Needs classification`
- **THEN** Project Web shows each idea with unknown exploration, decision, or evidence facets and identifies the unknown fields
- **AND** it does not hide or silently remap those ideas

### Requirement: Project Web Shows Kaoju Directions Through the Canonical Portfolio
Project Web SHALL present Kaoju survey-direction proposals through the same canonical Research Idea components, presets, lineage, decision review, detail, and steering flows used for every supported research paradigm.

#### Scenario: User opens a Kaoju-only topic
- **WHEN** a topic contains an actor-confirmed Kaoju Direction Set whose proposals have canonical Research Idea effects and contains no DeepSci ideas
- **THEN** Idea Graph and Idea Timeline show every eligible direction proposal with its canonical facets, selected or non-selected decision outcome, exact realization detail, and lineage
- **AND** Project Web does not require DeepSci installation, a Kaoju-specific view, or heuristic extraction

#### Scenario: User opens a mixed-paradigm topic
- **WHEN** a topic contains canonical Research Ideas produced by both Kaoju and DeepSci
- **THEN** the same portfolio view shows the union under one applied predicate, source count, index revision, and topology-completeness contract
- **AND** filtering by lifecycle state, decision, lineage, or text behaves independently of producing paradigm

#### Scenario: User reviews a Kaoju direction decision
- **WHEN** the user opens decision context for a Kaoju direction selected from an actor-confirmed Direction Set
- **THEN** Project Web shows the Direction Set Decision Record, every authored proposal option, each outcome, rationale, actor, timestamp, and current canonical facets
- **AND** an option that was not selected but remained open is not displayed as rejected, deferred, or closed

#### Scenario: User opens a Kaoju direction realization
- **WHEN** the user opens source detail from a Kaoju-derived Research Idea
- **THEN** Project Web lazily displays the exact proposal object and its Direction Set context through canonical detail refs
- **AND** it does not parse the Direction Set in the graph or timeline list component

#### Scenario: Legacy Kaoju projection is missing
- **WHEN** a legacy Direction Set has no canonical Research Idea projection
- **THEN** Project Web shows an incomplete-portfolio diagnostic and supported migration or repair action from backend metadata
- **AND** it does not silently omit the known gap or create authoritative browser-only ideas

### Requirement: Idea Graph and Timeline Share Portfolio Semantics
Project Web SHALL apply the same preset and facet vocabulary in Idea Graph and Idea Timeline while keeping their independent presentation and layout state.

#### Scenario: User switches between graph and timeline
- **WHEN** the same Research Topic is open in both Idea Graph and Idea Timeline
- **THEN** both views offer the same semantic presets and facet labels
- **AND** the same applied predicate produces the same eligible Research Idea ids when both views use the same complete source revision

#### Scenario: User composes filters
- **WHEN** a user combines a preset with exploration, decision, evidence, archive, visibility, relation-kind, text, generation, or decision filters
- **THEN** Project Web displays the composed predicate and visible-versus-source counts
- **AND** it offers a clear way to remove individual filters or restore the preset

#### Scenario: Filtered view is restored
- **WHEN** a restorable Idea Graph or Idea Timeline view reopens
- **THEN** Project Web restores its portfolio preset and explicit filters as GUI Runtime State or browser view state
- **AND** restoration does not write canonical Research Idea state

#### Scenario: Backend and local filtering agree
- **WHEN** Project Web uses local filtering for a complete lightweight graph and backend filtering for an incomplete or bounded graph
- **THEN** shared contract fixtures produce the same eligible idea ids and facet counts for equivalent source data and predicates

### Requirement: Idea Nodes Show Independent State Meaning
Project Web SHALL render exploration, decision, evidence, visibility, and archive meaning as independent visual or textual properties.

#### Scenario: Selected idea is unexplored
- **WHEN** an idea has decision state `selected` and exploration state `unexplored`
- **THEN** the node, row, hover, or detail view exposes both values without replacing one with the other

#### Scenario: Explored idea is deferred
- **WHEN** an idea has exploration state `explored` and decision state `deferred`
- **THEN** the view exposes both values and keeps its evidence assessment separate

#### Scenario: Evidence is refuted but idea remains open
- **WHEN** an idea has evidence state `refuted` and decision state `open`
- **THEN** Project Web shows the refuted assessment without styling the idea as closed

#### Scenario: Backend selection differs from UI selection
- **WHEN** a Research Idea has decision state `selected` but the user selects another node for inspection
- **THEN** backend decision styling and browser UI-selection styling remain distinct

### Requirement: Users Can Trace Research Idea Derivation
Project Web SHALL let users inspect canonical ancestors and descendants from a selected Research Idea.

#### Scenario: User shows all descendants
- **WHEN** a user selects a Research Idea and invokes `Show descendants`
- **THEN** Project Web requests or derives bounded descendant traversal over the selected relation kinds
- **AND** it shows traversal roots, completeness, depth, relation filters, and visible-versus-source counts

#### Scenario: User shows ancestry
- **WHEN** a user selects a Research Idea and invokes `Show ancestry`
- **THEN** Project Web requests or derives bounded ancestor traversal over canonical Idea Lineage Edges
- **AND** stored edge direction and relation labels remain visible

#### Scenario: Traversal is incomplete
- **WHEN** a traversal reaches a safety bound or the source topology is incomplete
- **THEN** Project Web labels the result incomplete and offers a supported refinement or continuation action
- **AND** it does not present the visible leaves as proven terminal ideas

#### Scenario: User exits traversal focus
- **WHEN** a user exits ancestor or descendant inspection
- **THEN** Project Web returns to the prior portfolio predicate and view state
- **AND** no canonical idea or lineage data changes

### Requirement: Users Can Review Selection Decisions
Project Web SHALL explain why an idea was selected by presenting the corresponding Decision Record and complete recorded alternative set.

#### Scenario: User asks why an idea was selected
- **WHEN** a user opens selection context for a selected Research Idea
- **THEN** Project Web shows the selected option, every recorded considered Research Idea, each outcome, rationale, consequences, deciding actor, timestamp, and supporting refs
- **AND** each option can open its Research Idea detail without losing the comparison context

#### Scenario: Historical decision context is incomplete
- **WHEN** a Decision Record lacks one or more considered alternatives or rationale fields
- **THEN** Project Web identifies the missing context explicitly
- **AND** it does not fill gaps from generation siblings, record prose, or current state

#### Scenario: Idea participated in several decisions
- **WHEN** a Research Idea appears in more than one Decision Record
- **THEN** Project Web presents the decision history in timestamp or sequence order
- **AND** it distinguishes current disposition from prior outcomes

### Requirement: Users Can Review Deferred and Closed Ideas
Project Web SHALL let users inspect deferred and closed Research Ideas together with the reason and evidence behind each disposition.

#### Scenario: User reviews deferred ideas
- **WHEN** a user selects the `Deferred` preset
- **THEN** Project Web shows deferred ideas and provides their deferral reason, deciding actor, timestamp, consequence, Decision Record, and reopen history when available

#### Scenario: User reviews closed ideas
- **WHEN** a user selects the `Closed` preset
- **THEN** Project Web shows closed ideas and distinguishes rejection, supersession, duplication, invalidation, user closure, and unknown legacy closure reasons

#### Scenario: User finds an idea worth reconsidering
- **WHEN** a user inspects a deferred or closed idea and chooses to reconsider it
- **THEN** Project Web offers the explicit `Explore this idea` or `Explore instead` steering flow with reopening consequences and rationale requirements
- **AND** merely opening or selecting the idea does not reopen it

### Requirement: Project Web Exposes Explicit Idea Steering
Project Web SHALL expose Research Idea steering as a confirmed action separate from graph selection and read-only inspection.

#### Scenario: User explores alongside current work
- **WHEN** a user invokes `Explore this idea` on an eligible Research Idea
- **THEN** the confirmation surface identifies the target idea, expected state changes, Research Task effect, and prompt sent through the Project Operator
- **AND** it does not imply that other selected ideas will be deferred or closed

#### Scenario: User explores instead
- **WHEN** a user invokes `Explore instead`
- **THEN** the confirmation surface requires the exact currently selected ideas to replace and the user's rationale
- **AND** it displays the proposed target and prior-selection state transitions before submission

#### Scenario: Steering succeeds
- **WHEN** a steering action returns accepted durable refs
- **THEN** Project Web refreshes affected idea, decision, task, and dispatch views through the new index revision
- **AND** it reports whether topic research actor dispatch was accepted, pending, or blocked

#### Scenario: Steering conflicts
- **WHEN** the canonical idea state changed after the confirmation surface loaded
- **THEN** Project Web shows the current state and requires the user to review the changed consequences
- **AND** it does not resubmit silently against stale state
