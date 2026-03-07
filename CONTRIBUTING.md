# Contributing to DeadlineHQ

Thank you for your interest in contributing to DeadlineHQ! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/deadlinehq.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the setup script:
```bash
python setup.py
```

3. Run tests to ensure everything works:
```bash
pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Use pytest fixtures for common test setup

Example test structure:
```python
def test_feature_name():
    """Test description."""
    # Arrange
    setup_data = create_test_data()
    
    # Act
    result = function_to_test(setup_data)
    
    # Assert
    assert result == expected_value
```

## Commit Messages

Use clear and descriptive commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add task priority filtering to search command
Fix email sending error when SMTP server is unavailable
Update README with new configuration options
```

## Pull Request Process

1. Update README.md with details of changes if applicable
2. Update tests to cover new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md (if exists) with notable changes
5. The PR will be merged once reviewed and approved

## Feature Requests

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Clearly describe the feature and its use case
3. Explain why this feature would be useful
4. Provide examples if possible

## Bug Reports

When reporting bugs, please include:

1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information (OS, Python version)
6. Relevant log files or error messages

## Areas for Contribution

Here are some areas where contributions would be particularly valuable:

### Features
- Recurring task support
- Task statistics and reporting
- Timezone support for deadlines
- Web interface
- Mobile notifications
- Task dependencies
- Calendar integration
- Export/import functionality

### Improvements
- Performance optimization
- Better error messages
- More comprehensive tests
- Documentation improvements
- Code refactoring

### Bug Fixes
- Check the issues page for known bugs
- Test edge cases and report issues

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. Maintainers will review your code
2. Feedback will be provided if changes are needed
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged in the project

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to DeadlineHQ!
