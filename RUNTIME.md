# CONSONORIUM RUNTIME

Runtime modes:
- inventory
- audit
- reconcile
- plan-repairs
- apply-mechanical-repairs
- publish-checks
- publish-epoch-candidate
- quarantine
- project

Boundary:
- consumes law from SYNTAGMARIUM
- consumes previous accepted state from ORBISTIUM
- emits contradiction, repair, quarantine, and epoch-candidate outputs
- does not author law
- does not become accepted state
