# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**qc-openmaterial-3d** is an ASAM QC Framework checker bundle that validates OpenMATERIAL 3D files (`.xoma`, `.xomm`, `.xomp`, `.xompt`) against the ASAM OpenMATERIAL 3D standard. It is part of the ASAM QC Framework ecosystem and produces XQAR (XML Quality Analysis Report) output.

## Commands

**Install:**
```bash
poetry install --with dev
```

**Run checker:**
```bash
poetry run qc_openmaterial -c config.xml
```

**Run all tests:**
```bash
poetry run pytest -vv
```

**Run a single test:**
```bash
poetry run pytest tests/test_xom_general_checks.py::test_valid_json_document_positive -vv
```

**Format code:**
```bash
poetry run black qc_openmaterial3d tests
```

**Pre-commit hooks:**
```bash
pre-commit install
pre-commit run --all-files
```

## Architecture

### Plugin-based checker design

Each rule is its own module under `qc_openmaterial3d/checks/xom_general_checker/`. A checker module must export:

- `CHECKER_ID` — unique string ID
- `CHECKER_DESCRIPTION` — human-readable description
- `CHECKER_PRECONDITIONS` — `set[str]` of checker IDs that must pass first (controls execution order)
- `RULE_UID` — ASAM rule reference string
- `check_rule(checker_data: CheckerData) -> None` — executes the check and adds issues to `checker_data`

Checkers are registered in `main.py` and executed by the ASAM QC base library.

### Data flow

1. `main.py` parses an XML config file, instantiates a `Result` object, registers checkers, and calls `run_checks()` from `asam-qc-baselib`.
2. Each checker receives a `CheckerData` object (`qc_openmaterial3d/checks/models.py`) containing the `Result` and the path to the file under test.
3. Checks report issues via `checker_data.result.add_issue(...)` with file location data from `find_property_line()` in `utils.py`.
4. The base library serialises results to `.xqar` XML format.

### Key modules

- `qc_openmaterial3d/main.py` — entry point; wires checkers to the framework
- `qc_openmaterial3d/checks/xom_general_checker/` — the four implemented checkers (valid JSON, version defined, valid schema, URIs exist)
- `qc_openmaterial3d/checks/models.py` — `CheckerData` dataclass and `AttributeType` enum
- `qc_openmaterial3d/checks/utils.py` — `compare_versions()`, `find_property_line()`, `parse_json()`
- `qc_openmaterial3d/basic_preconditions.py` — shared precondition constants
- `qc_openmaterial3d/schemas/` — embedded JSON schemas per OpenMATERIAL 3D version (currently `1.0.0/`)

### Tests

Tests live in `tests/test_xom_general_checks.py`. Each test:
1. Calls `test_utils.create_test_config()` to write a temporary XML config pointing at a fixture file under `tests/data/`.
2. Calls `test_utils.launch_main()` to run the checker.
3. Loads the resulting `tests/xom_bundle_report.xqar` and asserts issue counts/types.

Test fixture directories under `tests/data/` mirror checker names (`valid_json_document/`, `version_is_defined/`, `valid_schema/`, `uris_exist/`), each containing positive and negative cases.

### Version handling

`utils.compare_versions()` does semantic version comparison. Avoid string comparison for version fields — lexicographic ordering breaks `1.10.0 > 1.9.0`.

### Schema validation

JSON schemas are stored in `qc_openmaterial3d/schemas/<version>/` and selected at runtime based on `metadata.openMaterial3dVersion` in the input file. The `general_valid_schema` checker uses `jsonschema.Draft7Validator`.
