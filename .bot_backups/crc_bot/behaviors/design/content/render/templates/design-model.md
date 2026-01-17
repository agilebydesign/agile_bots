# Design Model

## Object-Oriented Design Patterns

### Domain Concepts with Responsibilities

{{#epics}}
## Epic: {{name}}

{{#domain_concepts}}
### {{name}}{{#inherits_from}} : {{inherits_from}}{{/inherits_from}}

**Instantiated with:** {{#instantiated_with}}{{.}}, {{/instantiated_with}}

**Responsibilities:**
{{#responsibilities}}
- {{name}}: {{#collaborators}}{{.}}, {{/collaborators}}
{{/responsibilities}}

**Ownership:**
- Has: {{#ownership.has}}{{.}}, {{/ownership.has}}
- References: {{#ownership.references}}{{.}}, {{/ownership.references}}

{{/domain_concepts}}
{{/epics}}

