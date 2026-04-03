# CONSONORIUM Runtime Doctrine

## Mission

CONSONORIUM turns observed Verifrax state into lawful or unlawful state classifications.

## Runtime modes

- inventory
- audit
- reconcile
- plan-repairs
- apply-mechanical-repairs
- publish-checks
- publish-epoch-candidate
- quarantine
- project

## Required boundaries

- law comes from SYNTAGMARIUM
- accepted state is written to ORBISTIUM
- runtime outputs do not redefine law
- runtime outputs do not become the only truth store

## Required subsystems

- collectors
- normalizers
- evaluators
- planners
- compilers
- publishers
- GitHub runtime integration

## Inventory candidate

`inventory` currently emits a deterministic sovereign-layer candidate containing repository nodes and dependency edges for the law, state, and runtime layer.
