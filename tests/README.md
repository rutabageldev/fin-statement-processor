# 🧪 Ledgerly Statement Processor — Test Suite

This folder contains all unit, edge case, and integration tests for the Ledgerly financial statement processing pipeline. Tests are written using [pytest](https://docs.pytest.org/en/stable/) and designed for incremental rollout across critical functionality.

---

## ✅ Testing Strategy

We implement tests in **five manageable phases** to progressively build confidence in the system while supporting rapid development and refactoring.

### COMPLETE **Phase 1: Core Happy Path**
- Validate PDF parsing, normalization, and core model construction.
- Establish fixtures and the testing framework.

### COMPLETE **Phase 2: Parser and Service Logic**
- Test edge cases in normalization and parsing.
- Validate dispatch logic.
- Add coverage for alternate parser types (e.g., CSV).

### **Phase 3: Model Validation**
- Test all models’ `.from_dict()` and `__init__()` methods.
- Ensure correct type conversion, required field handling, and failure cases.

### **Phase 4: Support Services**
- Test `parser_config_loader` and registry services.
- Use mocks for external file or service dependencies.

### **Phase 5: Integration + Redpanda Prep**
- Full end-to-end test of file parsing → normalization → data models.
- Prepare hooks for Redpanda and database output integration.

---

## 📁 Directory Structure

```bash
tests/
├── conftest.py                         # Shared fixtures
├── test_main.py                        # Top-level flow tests
├── normalization/
│   └── test_normalization.py
├── parsers/
│   ├── test_dispatch_parser.py
│   ├── pdf/
│   │   └── test_parse_citi_cc_pdf.py
│   └── csv/
│       └── test_parse_citi_cc_csv.py
├── parser_config/
│   └── test_parser_config_loader.py
├── models/
│   ├── test_debt_details.py
│   ├── test_statement.py
│   └── test_transactions.py
├── registry/
│   └── test_registry_loader.py
└── README.md
