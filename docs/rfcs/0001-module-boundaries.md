# RFC 0001: Module boundaries

- Status: Draft
- Authors: ChatGPT
- Created: 2024-05-??

## Summary

Define clear module boundaries for the chat simulator and outline small refactor steps to reach the target layout.

## Motivation

Current code mixes domain logic with framework and infrastructure details. Establishing modules will reduce coupling and enable parallel development.

## Proposal

Adopt the module layout described in `DOMAIN.md` (`core/`, `adapters/`, `cli/`, `web/`, `storage/`). Perform a sequence of focused pull requests:

1. **Extract domain models to `core/`**  
   Move data models and agent logic from `backend/app/models` and `backend/chatagent/agents`.  
   _Proposed Issue: "Refactor: move models and agents to core" (medium impact: ~10 files)_

2. **Isolate CLI into `cli/` package**  
   Relocate `backend/chatagent/cli.py` and define an explicit entry point.  
   _Proposed Issue: "Refactor: separate CLI module" (low impact: ~3 files)_

3. **Split FastAPI web app into `web/`**  
   Move `backend/chatagent/app.py`, templates, and static assets.  
   _Proposed Issue: "Refactor: extract web module" (medium impact: ~8 files)_

4. **Create `storage/` for persistence**  
   Group `backend/chatagent/db` and `services/persistence.py` under a storage interface.  
   _Proposed Issue: "Refactor: unify storage layer" (medium impact: ~6 files)_

5. **Introduce adapters for external services**  
   Relocate provider and tool implementations to `adapters/` while keeping abstract interfaces in `core/`.  
   _Proposed Issue: "Refactor: migrate providers/tools to adapters" (high impact: ~12 files)_

## Alternatives

Continue with the flat structure. This risks tight coupling and harder testing as features grow.

## Unresolved Questions

- Exact package names may evolve.
- Additional modules (e.g., `ui/`) could emerge as functionality grows.

## References

- [`docs/DOMAIN.md`](../DOMAIN.md)
