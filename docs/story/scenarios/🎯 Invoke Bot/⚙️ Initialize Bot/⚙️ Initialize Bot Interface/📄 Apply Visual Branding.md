# 📄 Apply Visual Branding

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/initialize_bot/test_initialize_bot_interface.py)

**User:** Panel
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Initialize Bot](..) / [⚙️ Initialize Bot Interface](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Apply Visual Branding functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel initializes
  **then** Panel loads branding config from conf/config.json

- **When** branding property specifies brand name
  **then** Panel activates that brand's settings

- **When** Panel generates webview
  **then** Panel injects CSS variables from brand colors (--bg-base, --text-color, --accent-color, --text-color-faded, --font-weight-normal)

- **When** brand has path property
  **then** Panel loads images from that subdirectory

- **When** Header renders
  **then** Header displays product name from brand title
  **and** applies brand accent color to title

- **When** config file missing
  **then** Panel uses default ABD branding BUT does not crash

- **When** background is light (#FFFFFF)
  **then** Panel uses dark overlays for hover states

- **When** background is dark (#000000)
  **then** Panel uses light overlays for hover states

- **When** branding loads
  **then** branding caches config for subsequent calls

## Scenarios

<a id="scenario-panel-applies-default-agile-by-design-branding-when-no-config-entry-exists"></a>
### Scenario: [Panel applies default Agile By Design branding when no config entry exists](#scenario-panel-applies-default-agile-by-design-branding-when-no-config-entry-exists) (edge)

**Steps:**
```gherkin
GIVEN: Config file missing OR branding property not set OR repo root not set
WHEN: Panel initializes with workspace root
THEN: Branding module logs warning about missing config
AND: Branding module returns default ABD settings
WHEN: Panel generates webview content
THEN: Panel injects --bg-base as #000000 (dark background)
AND: Panel injects --text-color as #FFFFFF
AND: Panel injects --accent-color as #FF8C00 (orange)
AND: Panel injects --font-weight-normal as 400
AND: Panel sets --hover-bg to light overlay for dark background
WHEN: Header view renders
THEN: Header displays 'Agile Bots' as product name
AND: Header loads images from default img/ directory
BUT: Panel does not crash or show error
```


<a id="scenario-panel-applies-scotia-branding-when-config-specifies-scotia-brand"></a>
### Scenario: [Panel applies Scotia branding when config specifies Scotia brand](#scenario-panel-applies-scotia-branding-when-config-specifies-scotia-brand) (happy)

**Steps:**
```gherkin
GIVEN: Config file exists at conf/config.json with branding property set to 'Scotia'
WHEN: Panel initializes with workspace root
THEN: Branding module reads conf/config.json
AND: Branding module caches config for subsequent calls
AND: Panel logs 'Scotia' as active branding
WHEN: Panel generates webview content
THEN: Panel injects --bg-base as #FFFFFF (light background)
AND: Panel injects --text-color as #000000
AND: Panel injects --accent-color as #EC111A (Scotia red)
AND: Panel injects --font-weight-normal as 600
AND: Panel sets --hover-bg to dark overlay for light background
WHEN: Header view renders
THEN: Header displays 'Scotia Bots' as product name
AND: Header applies Scotia red to title style
AND: Header loads images from img/scotia/ subdirectory
```

