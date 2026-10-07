# Pharma Bottle Vision Inspection System

An industrial computer-vision system for automated quality inspection of
pharmaceutical syrup bottles on a high-speed production conveyor.

---

## System Overview

This system provides end-to-end automated visual inspection of syrup
bottles, replacing manual quality checks with deterministic machine-vision
and AI-based inspection. Every bottle is individually imaged, analysed, and
verdict-classified as **PASS** or **FAIL** within a strict per-bottle budget.

---

## Target Production Speed

| Metric | Value |
|---|---|
| Throughput | 120 bottles / minute |
| Cycle time | ~500 ms per bottle |
| Bottle spacing | ~250 mm centre-to-centre |

---

## Inspection Capabilities

The system will inspect the following attributes on each bottle:

| # | Inspection | Description |
|---|---|---|
| 1 | **Cap presence** | Detect missing caps |
| 2 | **Cap seating / alignment / tilt** | Verify cap is fully seated and within angular tolerance |
| 3 | **Tamper ring** | Check for intact / broken tamper-evident ring |
| 4 | **Liquid fill level** | Measure fill height against upper / lower tolerance bounds |
| 5 | **Label presence & position** | Confirm label is present and correctly placed |
| 6 | **Packaging defects** | Surface defects, scratches, air bubbles, label print quality |
| 7 | **OCR (optional)** | Lot number, expiry date, batch ID — opt-in per recipe |
| 8 | **Final PASS/FAIL decision** | Aggregated verdict from all active inspections |
| 9 | **PLC / reject synchronisation** | Signal pneumatic reject at the correct conveyor position |

---

## High-Level Architecture

```
 ┌─────────────┐        ┌──────────────────┐        ┌──────────────┐
 │  PLC / HMI  │◄──────►│  Vision System   │◄──────►│  Camera(s)   │
 │  (Modbus)   │        │  (Host PC / GPU) │        │  (GigE/IP)   │
 └─────────────┘        └──────┬──┬──┬──┬──┘        └──────────────┘
                              │  │  │  │
                       ┌──────┘  │  │  └──────┐
                       │         │  │         │
              ┌────────┴─┐  ┌────┴──┴──┐  ┌───┴──────────┐
              │ Inspection│  │ Decision │  │     PLC      │
              │ Pipeline  │  │ Engine   │  │Reject Scheduler│
              │(preprocess│  │(rules,   │  │(conveyor     │
              │ + AI +    │  │ recipe)  │  │ delay calc)   │
              │ modules)  │  │          │  │              │
              └────┬──────┘  └────┬─────┘  └───────┬──────┘
                   │              │                │
          ┌────────┴──────────────┴────────────────┴───────┐
          │              Storage Layer                      │
          │ (SQLite / PostgreSQL + Evidence + CSV Export)  │
          └────────┬───────────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │    Dashboard    │
          │ (real-time UI)  │
          └─────────────────┘
```

---

## Folder Structure

| Path | Purpose |
|---|---|
| `app/` | Application core: entry point, configuration, logging |
| `cameras/` | Camera abstraction layer (industrial, RTSP, trigger) |
| `inspection/` | Inspection pipeline, preprocessing, per-module inspections |
| `ai/` | Deep-learning model wrappers (detector, segmenter, model manager) |
| `decision/` | Quality-decision engine (rules, recipes, result objects) |
| `plc/` | PLC communication client and reject-scheduler logic |
| `storage/` | Database models, repository access, CSV/report export |
| `ui/` | Real-time dashboard and reusable UI widgets |
| `tools/` | Utility scripts and maintenance helpers |
| `tests/` | Unit and integration tests |
| `models/` | (git-ignored) AI model weights and checkpoints |
| `data/` | (git-ignored) Generated / runtime data files |
| `evidence/` | (git-ignored) Captured PASS/FAIL evidence images |
| `logs/` | (git-ignored) Application and audit log files |
| `configs/` | (git-ignored) Runtime configuration files |
| `scripts/` | (git-ignored) Setup, calibration, and operational scripts |
| `docs/` | (git-ignored) Supplementary documentation |
| `main.py` | Root entry point — delegates to `app.main.main` |
| `requirements.txt` | Placeholder dependency list (unpinned) |
| `requirements-lock.txt` | Pinned lock file (to be generated) |
| `.env.example` | Template for required environment variables |
| `.gitignore` | Python, OS, IDE, model, log, and evidence ignore rules |

---

## Development Phases

| Phase | Scope | Status |
|---|---|---|
| 0 | Project scaffold & structure initialization | ✅ In progress |
| 1 | Dependency installation & environment validation | Planned |
| 2 | Configuration, logging, camera abstraction layer | Planned |
| 3 | AI model manager & inference wrappers | Planned |
| 4 | Inspection modules & pipeline orchestration | Planned |
| 5 | Decision engine, PLC integration, storage layer | Planned |
| 6 | Dashboard & reporting | Planned |
| 7 | Testing, validation, and deployment prep | Planned |

---

## Engineering Principles

- **Thread safety & determinism** — all shared state is designed for
  concurrent access under strict per-bottle timing constraints.
- **Fail-safe defaults** — any unhandled inspection error results in a
  **FAIL** verdict (reject the bottle) rather than risking a defective
  product shipping.
- **Separation of concerns** — camera I/O, AI inference, decision logic,
  PLC I/O, and storage are strictly decoupled through well-defined
  interfaces and value objects.
- **Evidence retention** — every FAIL (and sampled PASS) is associated
  with a saved evidence image and full parameter log for traceability.
- **Auditability** — all decisions, model versions, and system events are
  recorded in append-only audit logs.
- **Configurability** — product-specific parameters live in loadable
  *recipes*, not hardcoded defaults.
- **Reproducibility** — dependency versions are pinned via
  `requirements-lock.txt`; model versions are tracked in the model
  manager.

---

## Current Status

> **Project structure initialized.**  
> No application logic, camera code, PLC code, AI models, or fake
> implementations have been added at this stage.

Dependency versions have **not** been selected or pinned yet — they will
be resolved and validated with `pip-compile` in the next setup phase,
producing the final `requirements-lock.txt`.

---

## License

Proprietary — Pharmaceutical Quality Assurance Engineering Team.
