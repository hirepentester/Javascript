# Contributing to ML JavaScript Analyzer

## Pull Requests

Pull requests must always be opened from a branch of `Javascript`, even if you have
commit rights to the repository so that all contributors follow the same process.

## Development Workflow

1. Create a feature branch from `working` branch
2. Make your changes and test locally
3. Push to your feature branch
4. Create a Pull Request to `working` branch
5. After approval, merge to `working` → `staging` → `deploy`

See [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md) for detailed branching guidelines.

## Testing

Before submitting a PR:

```bash
# Run tests
pytest test_main.py -v

# Run linting
flake8 .
pylint src/

# Test analysis
python ml_analyzer.py --analyze-all
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and concise
