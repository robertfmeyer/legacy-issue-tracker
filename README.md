# Legacy Issue Tracker – Modernization Portfolio

This repository demonstrates how to **analyze, refactor, and modernize a legacy backend system safely and incrementally**, while preserving behavior and managing risk.

It is intentionally structured to show:
- how legacy systems often evolve,
- how to make them safe to change,
- and how to modernize them without a risky rewrite.

This project is designed as a **portfolio artifact**, not a production-ready service.

---

## Project Structure

legacy-issue-tracker/
├── legacy_app/ # Intentionally legacy implementation
├── modern_app/ # Refactored, modular, testable version
├── docs/ # Design notes and modernization decisions
└── README.md


---

## Goals of This Project

- Demonstrate real-world **legacy code analysis**
- Apply **incremental refactoring techniques**
- Preserve behavior using **characterization tests**
- Improve maintainability, structure, and clarity
- Show engineering judgment around tradeoffs and scope

This mirrors the kinds of systems engineers inherit in production environments.

---

## Legacy Implementation

The `legacy_app/` directory contains a deliberately flawed backend service with characteristics commonly found in legacy systems:

- Mixed concerns (API, business logic, persistence)
- JSON file used as a datastore
- Minimal validation
- No caching
- Stringly-typed business rules
- Limited error handling

The goal is **not** to criticize this code, but to treat it as a realistic starting point.

---

## Modern Implementation

The `modern_app/` directory contains a refactored version of the system with:

- Clear separation of concerns
- Testable business logic
- Repository and service layers
- Explicit data models
- Caching for frequently accessed data
- Improved error handling and structure

Refactoring is done incrementally to reduce risk.

---

## Documentation

Additional documentation lives in `docs/`:

- `modernization_plan.md` – step-by-step refactoring plan
- `decisions.md` – key design and tradeoff decisions
- `api_examples.md` – example API usage

---

## What This Project Demonstrates

- Legacy system comprehension
- Refactoring without breaking behavior
- Pragmatic backend design
- Testing strategies for unsafe code
- Engineering communication through documentation

---

## What This Project Is Not

- A greenfield demo app
- A framework showcase
- A production deployment

It is intentionally scoped to focus on **engineering judgment and refactoring skill**.

---

## Future Work (Out of Scope for Initial Version)

- Authentication and authorization
- Persistent database storage
- Observability and metrics
- Horizontal scaling

These are noted but intentionally deferred.















