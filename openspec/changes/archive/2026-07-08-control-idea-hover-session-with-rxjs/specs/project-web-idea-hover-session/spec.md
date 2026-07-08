## ADDED Requirements

### Requirement: Idea Hover Uses Session-Based Event Ordering
The Project Web idea lineage graph SHALL treat a pointer hover over an idea node as a bounded hover session that starts on node enter and ends on node leave.

#### Scenario: Hover delay starts on node enter
- **WHEN** a user moves the pointer into an idea lineage graph node
- **THEN** the graph SHALL start one hover session for that node and arm the configured hover preview delay for that session

#### Scenario: Hover session ends on node leave
- **WHEN** the pointer leaves the node and its active hover preview area
- **THEN** the graph SHALL end the active hover session and close or cancel its hover preview through the normal cleanup behavior

### Requirement: Click Terminates Current Hover Session
The Project Web idea lineage graph SHALL treat a node click as a terminal event for the current hover session on that node.

#### Scenario: User clicks before hover delay elapses
- **WHEN** a user enters an idea node and clicks that node before the hover delay elapses
- **THEN** the graph SHALL cancel the pending hover preview for that hover session
- **AND** no hover preview SHALL appear until the user leaves the node and enters it again

#### Scenario: User clicks while hover preview is visible
- **WHEN** a user clicks an idea node while that node's hover preview is visible
- **THEN** the graph SHALL close the visible hover preview
- **AND** no hover preview SHALL reappear for the same hover session

#### Scenario: User moves within node after click
- **WHEN** a user clicks an idea node and then moves the pointer within the same node without leaving it
- **THEN** the graph SHALL NOT rearm the hover preview delay for that hover session

#### Scenario: User leaves and re-enters after click
- **WHEN** a user clicks an idea node, leaves the node, and later enters the same node again
- **THEN** the graph SHALL allow a new hover session to arm the hover preview delay

### Requirement: Hover Timing Is Owned by RxJS Boundary
The Project Web idea lineage graph SHALL use a named RxJS event boundary or feature effect to coordinate hover delay, click cancellation, leave cancellation, tooltip close, and stale timer suppression.

#### Scenario: Component publishes semantic pointer events
- **WHEN** React Flow reports node enter, move, leave, click, double-click, or touch long-press events
- **THEN** the idea lineage graph component SHALL publish typed semantic events or typed actions instead of directly coordinating hover timers in rendering handlers

#### Scenario: Stale delayed event arrives
- **WHEN** a delayed hover event is emitted after its hover session has ended or been canceled
- **THEN** the interaction state SHALL ignore that stale event and SHALL NOT show a hover preview

#### Scenario: Double click opens idea
- **WHEN** a user double-clicks an idea node to open it
- **THEN** the graph SHALL close or cancel the active hover session before emitting the open intent

### Requirement: Existing Preview Capabilities Are Preserved
The Project Web idea lineage graph SHALL preserve existing hover preview rendering behavior while changing event ownership and cancellation semantics.

#### Scenario: Hover preview becomes visible
- **WHEN** a user enters an idea node and does not click or leave before the configured hover delay elapses
- **THEN** the graph SHALL show the existing bounded Markdown-capable hover preview for that node

#### Scenario: Touch long press opens preview
- **WHEN** a user long-presses an idea lineage graph node on a touch interface without canceling the gesture
- **THEN** the graph SHALL show the same bounded Markdown-capable hover preview as before
