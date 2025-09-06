# 🛠️ Ruff Technical Debt Roadmap

## Executive Summary

This document outlines a prioritized approach to addressing the 37 ignored ruff rules in our `ruff.toml` configuration. The project currently has ~2,359 lines of Python code across 49 files, making this a manageable but important technical debt cleanup effort.

**Current State**: 34 ignored rules across multiple categories (down from 37)
**Progress**: Phase 1.1 and 1.3 completed (5 rules eliminated, 7 violations fixed)
**Target State**: Minimal ignores (only formatter conflicts and legitimate exceptions)
**Estimated Timeline**: 4-6 sprints (8-12 weeks)

---

## 📊 Impact Analysis

Based on violation counts and codebase analysis:

| Category                 | Current Violations | Effort Level | Business Impact          |
| ------------------------ | ------------------ | ------------ | ------------------------ |
| **Documentation**        | 47 violations      | Medium       | High (maintainability)   |
| **Logging & Exceptions** | 44 violations      | Low          | High (observability)     |
| **Code Quality**         | 7 violations       | Low          | Medium (maintainability) |
| **Type Safety**          | 4 violations       | Medium       | Medium (reliability)     |
| **Security**             | Unknown            | High         | High (compliance)        |

---

## 🎯 Phase-Based Roadmap

### **Phase 1: Quick Wins & Safety** (Sprint 1-2) — ⚠️ IN PROGRESS

_Focus: High-impact, low-effort improvements_

#### ✅ 1.1 Code Quality Cleanup — COMPLETED

**Fixed and removed from ignores:**

- Multiple pathlib modernization fixes (PTH103, PTH120, PTH123)
- Type annotation improvements (ANN001, ANN201)
- Deprecated rule cleanup (ANN101, ANN102, CPY)

**Status**: ✅ 7 violations fixed, 5 ignore rules eliminated

#### 1.2 Logging & Exception Improvements — REMAINING WORK

**Still need to remove these ignores:**

- `G004` - Logging f-string usage (34 violations) - Still ignored
- `EM101` - Raw string in exception (1 violation) - Still ignored
- `EM102` - F-string in exception (5 violations) - Still ignored
- `TRY003` - Vanilla exception args (4 violations) - Still ignored
- `F841` - Unused variables (4 violations) - Still ignored
- `ARG001` - Unused function arguments (3 violations) - Still ignored

**Benefits**: Better error messages and logging consistency
**Risk**: Low - mostly formatting changes

#### ✅ 1.3 Import & Path Modernization — COMPLETED

**Completed:**

- Replaced relative import in PDF parser with absolute import (TID252)
- Verified no remaining PTH118 issues; kept Path.open usage
- Removed `PTH118` and `TID252` from `ruff.toml` ignores

**Benefits**: Modern Python practices, better path handling
**Risk**: Very low

---

### **Phase 2: Type Safety & Annotations** (Sprint 3)

_Focus: Improving type safety without breaking changes_

#### 2.1 Type Annotation Improvements (Effort: 3-4 days)

**Remove these ignores:**

- `ANN401` - Disallow `Any` type (1 violation)
- `RUF012` - Mutable class attributes need ClassVar (0 violations currently)

**Benefits**: Better type safety, improved IDE support
**Risk**: Low - mostly adding annotations

#### 2.2 DateTime Handling (Effort: 2 days)

**Remove these ignores:**

- `DTZ001` - datetime() without tzinfo (unknown violations)
- `DTZ007` - strptime() without %z (unknown violations)
- `DTZ003` - datetime.utcnow() usage (unknown violations)

**Benefits**: Proper timezone handling, fewer datetime bugs
**Risk**: Medium - requires understanding business requirements

---

### **Phase 3: Documentation & Maintainability** (Sprint 4)

_Focus: Long-term maintainability_

#### 3.1 Documentation Coverage (Effort: 5-7 days)

**Selectively remove these ignores:**

- `D100` - Missing module docstrings (14 violations)
- `D101` - Missing class docstrings (6 violations)
- `D102` - Missing method docstrings (6 violations)
- `D103` - Missing function docstrings (16 violations)
- `D104` - Missing package docstrings (5 violations)

**Strategy**: Start with public APIs and core business logic
**Benefits**: Better code understanding, easier onboarding
**Risk**: Low - documentation only

#### 3.2 Code Complexity (Effort: 2-3 days)

**Remove these ignores:**

- `PLR0913` - Too many function arguments (2 violations)
- `PLR0911` - Too many return statements (1 violation)

**Benefits**: More maintainable functions
**Risk**: Medium - may require refactoring

---

### **Phase 4: Security & Advanced Quality** (Sprint 5-6)

_Focus: Security and advanced code quality_

#### 4.1 Security Improvements (Effort: 3-5 days)

**Remove these ignores:**

- `BLE001` - Blind exception catching (unknown violations)
- `B017` - Assert blind exception (unknown violations)

**Benefits**: Better error handling, fewer security risks
**Risk**: Medium - requires careful exception handling review

#### 4.2 Testing & Error Handling (Effort: 2-3 days)

**Remove these ignores:**

- `PT011` - pytest.raises() too broad (unknown violations)
- `TRY301` - Abstract raise to inner function (unknown violations)
- `TRY401` - Redundant exception in logging.exception (unknown violations)

**Benefits**: Better test quality, cleaner error handling
**Risk**: Low to medium

#### 4.3 Advanced Code Quality (Effort: 2-4 days)

**Remove these ignores:**

- `PGH003` - Use specific rule codes for type issues (unknown violations)
- `INP001` - Missing **init**.py files (unknown violations)

**Benefits**: Better tooling integration, cleaner package structure
**Risk**: Low

---

## 🚫 Permanent Ignores (Keep These)

These ignores should remain permanently as they conflict with our tooling or are intentional design decisions:

```toml
ignore = [
    # Formatter conflicts - KEEP THESE
    "COM812",  # Trailing comma missing (conflicts with formatter)
    "ISC001",  # Implicit string concatenation (conflicts with formatter)
    "E501",    # Line too long (handled by formatter)

    # TODO management - KEEP THESE (optional)
    "TD002",   # Missing author in TODO
    "TD003",   # Missing issue link in TODO
    "FIX002",  # Line contains TODO

    # Test-specific ignores (handled in per-file-ignores)
    # Move these to per-file-ignores if not already there
]
```

---

## 📋 Implementation Strategy

### For Each Phase:

1. **Pre-work**: Run `ruff check --select [RULE_CODES]` to see current violations
2. **Fix**: Address violations systematically
3. **Remove**: Remove the ignore from `ruff.toml`
4. **Verify**: Run full test suite
5. **Document**: Update this roadmap with completion status

### Automation Opportunities:

- **Auto-fixable rules**: Use `ruff check --fix --select [RULE_CODES]`
- **Batch processing**: Group similar rule types together
- **CI Integration**: Add ruff checks to prevent regression

### Risk Mitigation:

- **Feature branch**: Work on dedicated branches per phase
- **Incremental**: One or two rules at a time
- **Testing**: Full test suite after each rule removal
- **Rollback plan**: Keep git history for easy reversion

---

## 📈 Success Metrics

- **Rules Addressed**: Track progress from 37 → target of ~10 permanent ignores
- **Code Quality**: Monitor complexity metrics and test coverage
- **Developer Experience**: Measure time to understand/modify code
- **Bug Reduction**: Track issues related to ignored rule categories

---

## 🎯 Next Actions

1. **Immediate (Current Sprint)**:
   - [ ] Complete Phase 1.2 - Remove remaining logging/exception ignores (`G004`, `EM101`, `EM102`, `TRY003`, `F841`, `ARG001`)
   - [ ] Set up automated ruff checks in CI/CD pipeline

2. **Planning**:
   - [ ] Schedule dedicated time for technical debt work
   - [ ] Assign ownership for each phase
   - [ ] Set up metrics tracking

3. **Communication**:
   - [ ] Share roadmap with team
   - [ ] Get buy-in for dedicated technical debt sprints
   - [ ] Establish regular progress reviews

---

_Last Updated: September 6, 2025_
_Next Review: After Phase 1.2 completion_
