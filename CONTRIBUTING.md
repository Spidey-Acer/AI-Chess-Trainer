# Contributing to AI Chess Trainer

Thank you for your interest in contributing!

## Code of Conduct

Be respectful, collaborative, and constructive.

## How to Contribute

### Reporting Bugs
1. Check existing issues first
2. Use the bug report template
3. Include reproduction steps
4. Attach logs if relevant

### Suggesting Features
1. Check feature roadmap
2. Describe the use case
3. Explain why it's useful
4. Consider implementation complexity

### Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit PR with clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Chess-Trainer.git
cd AI-Chess-Trainer

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Stockfish
# macOS: brew install stockfish
# Linux: apt-get install stockfish
# Windows: Download from stockfishchess.org

# Run tests
pytest

# Run linters
black src/ tests/
flake8 src/
mypy src/
```

## Coding Standards

### Python
- Follow PEP 8
- Use type hints
- Write docstrings
- Max line length: 100
- Use Black formatter

### JavaScript/React
- Use ES6+ syntax
- Follow Airbnb style guide
- Use functional components
- PropTypes or TypeScript

### Commits
- Use conventional commits
- Clear, descriptive messages
- Reference issues when applicable

Example:
```
feat(analysis): add blunder detection
fix(ui): correct board orientation
docs: update API reference
test: add coverage for game analyzer
```

## Testing

- Write tests for new features
- Maintain >80% coverage
- Run full test suite before PR
- Include integration tests where appropriate

```bash
# Run tests
pytest

# With coverage
pytest --cov=src tests/

# Specific test
pytest tests/test_game_analyzer.py
```

## Documentation

- Update README for major features
- Add docstrings to functions/classes
- Update API.md for API changes
- Create examples for complex features

## Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Address feedback
4. Maintainer merges when ready

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Create a discussion on GitHub
- Check FAQ.md
- Contact maintainers

Thank you for contributing! 🎉
