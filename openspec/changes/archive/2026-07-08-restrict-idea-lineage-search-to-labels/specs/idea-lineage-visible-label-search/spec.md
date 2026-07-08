## ADDED Requirements

### Requirement: Idea Lineage Search Matches Visible Node Labels
The idea lineage graph SHALL filter nodes using only the text visibly rendered on each node label.

#### Scenario: User searches a visible acronym
- **WHEN** a user searches `ncu`
- **THEN** the graph SHALL keep only nodes whose visible label contains `ncu` after case-insensitive normalization
- **AND** nodes that only match hidden metadata SHALL be hidden

#### Scenario: User searches hidden metadata
- **WHEN** a user searches a record id, source JSON path, URL, realization id, topic id, or other hidden graph metadata
- **THEN** the graph SHALL NOT keep a node visible unless that text also appears in the node's visible label

### Requirement: Idea Lineage Search Uses Normalized Label Tokens
The idea lineage graph SHALL normalize visible labels and query text before matching, treating punctuation and repeated whitespace as separators.

#### Scenario: User searches separated label words
- **WHEN** a user searches multiple words that appear in different positions of a visible node label
- **THEN** the graph SHALL keep nodes whose normalized visible label contains every normalized query term

#### Scenario: User searches across punctuation
- **WHEN** a user searches words separated by spaces that correspond to hyphenated or punctuated label text
- **THEN** the graph SHALL treat those words as matching the visible label after normalization

#### Scenario: User clears the search
- **WHEN** a user clears the idea lineage search input
- **THEN** the graph SHALL restore the unfiltered idea lineage overview

### Requirement: Label Search Preserves Node-Only Filtering
The idea lineage graph SHALL filter nodes by visible labels and derive visible edges from the resulting node set.

#### Scenario: Search hides an endpoint
- **WHEN** label search hides a node
- **THEN** every edge attached to that hidden node SHALL also be hidden
- **AND** edge labels, relation kinds, and relationship metadata SHALL NOT independently keep a node visible
