## ADDED Requirements

### Requirement: Plugin Status Gates Plugin-Installed Callbacks
The system SHALL honor effective User Plugin status when resolving callbacks installed from user-plugin manifests.

#### Scenario: Enabled plugin callback resolves normally
- **WHEN** an active callback record has `plugin_id` metadata and the effective User Plugin status for the selected Project, Research Topic, Topic Actor, or Topic Agent context is `active`
- **THEN** callback resolution may include that callback when its target skill and stage match the request

#### Scenario: Disabled plugin callback is skipped
- **WHEN** an active callback record has `plugin_id` metadata and the effective User Plugin status for the selected context is disabled
- **THEN** callback resolution excludes that callback without deleting or mutating the callback registry record

#### Scenario: Missing plugin registration preserves existing callbacks
- **WHEN** an active callback record has `plugin_id` metadata but no applicable User Plugin registration exists
- **THEN** callback resolution treats the callback as enabled for backward compatibility and may include a diagnostic or source note that no plugin registration was found

#### Scenario: Disablement is context-specific
- **WHEN** a User Plugin is disabled for one Topic Actor or Topic Agent but remains enabled at the broader Research Topic or Project scope
- **THEN** callback resolution skips the plugin's callbacks only for the disabled effective context and continues resolving them for other contexts where the plugin remains enabled

#### Scenario: Callback list explains plugin gating
- **WHEN** a callback list, resolve, show, or validate command reports plugin-installed callbacks
- **THEN** the output includes enough plugin status metadata to explain whether the callback is effective, gated off, or missing plugin registration for the selected context
