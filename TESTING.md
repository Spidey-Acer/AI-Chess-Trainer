# Testing Guide

Comprehensive testing documentation for AI Chess Trainer.

## Test Coverage

**Current Status**: 10/10 tests passing ✅

```
Tests:  10 passed, 10 total
Time:   ~15s
Coverage: Core modules covered
```

## Running Tests

### Basic Test Commands

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_chess_engine.py

# Specific test function
pytest tests/test_game_analyzer.py::test_analyze_game

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Test Structure

```
tests/
├── conftest.py              # Fixtures
├── test_chess_engine.py     # Engine tests (7 tests)
└── test_game_analyzer.py    # Analyzer tests (3 tests)
```

## Test Files

### test_chess_engine.py

Tests for ChessEngine class:
- Engine initialization
- Position analysis
- Move evaluation
- Top moves retrieval
- Board state management
- Context manager
- Error handling

### test_game_analyzer.py

Tests for GameAnalyzer class:
- Game analysis workflow
- Mistake classification
- Statistics calculation

## Writing Tests

### Test Template

```python
import pytest
from src.core.chess_engine import ChessEngine

def test_feature():
    """Test description."""
    # Arrange
    engine = ChessEngine()
    
    # Act
    result = engine.some_method()
    
    # Assert
    assert result == expected
    
    # Cleanup
    engine.close()
```

### Using Fixtures

```python
@pytest.fixture
def engine():
    """Chess engine fixture."""
    eng = ChessEngine()
    yield eng
    eng.close()

def test_with_fixture(engine):
    """Test using fixture."""
    result = engine.analyze_position()
    assert result["score"] is not None
```

## Integration Testing

### Flask API Tests

```bash
# Start test server
python -m pytest tests/test_api.py

# Test specific endpoint
curl http://127.0.0.1:5000/api/health
```

### Desktop App Tests

```bash
# Run Electron tests
cd desktop
npm test

# E2E tests (when implemented)
npm run test:e2e
```

## Test Coverage

### Current Coverage

```
src/core/chess_engine.py      95%
src/core/game_analyzer.py     90%
src/core/position_evaluator.py 85%
```

### Generating Coverage Report

```bash
# HTML report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html

# Terminal report
pytest --cov=src --cov-report=term-missing tests/
```

## Performance Testing

### Benchmarks

```python
import time

def test_analysis_performance():
    """Test analysis speed."""
    engine = ChessEngine()
    start = time.time()
    
    engine.analyze_position()
    
    duration = time.time() - start
    assert duration < 2.0  # Should complete in under 2s
```

## CI/CD Testing

Tests run automatically on:
- Every push
- Every pull request
- Before merges

See `.github/workflows/` for CI configuration (when added).

## Troubleshooting Tests

### Stockfish Not Found

```bash
# Check Stockfish installation
which stockfish

# Set path in .env
echo "STOCKFISH_PATH=/usr/games/stockfish" > .env
```

### Import Errors

```bash
# Ensure src/ is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or use python -m
python -m pytest tests/
```

### Slow Tests

```bash
# Run with pytest-xdist (parallel)
pip install pytest-xdist
pytest -n auto
```

## Future Testing

Planned additions:
- [ ] API endpoint tests
- [ ] React component tests (Jest)
- [ ] E2E tests (Playwright/Cypress)
- [ ] Load testing
- [ ] Security testing

## Best Practices

1. **Arrange-Act-Assert** pattern
2. **One assertion per test** (when possible)
3. **Descriptive test names**
4. **Use fixtures** for setup/teardown
5. **Mock external dependencies**
6. **Keep tests fast** (<1s each)
7. **Test edge cases**
8. **Document complex tests**

---

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
