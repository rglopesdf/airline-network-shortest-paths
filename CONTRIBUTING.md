# Contributing to Airline Network Shortest Paths

We welcome contributions from the community! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/airline-network-shortest-paths.git
cd airline-network-shortest-paths

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Use type hints where appropriate
- Write docstrings for all public functions and classes

## Testing

- Write unit tests for new functionality
- Ensure all tests pass: `pytest`
- Maintain test coverage above 80%
- Include integration tests for complex features

## Documentation

- Update documentation for new features
- Use clear, concise language
- Include code examples where helpful
- Update README.md if necessary

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests as needed
3. Update documentation
4. Ensure all tests pass
5. Write a clear pull request description
6. Link to any relevant issues

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)
- Relevant code snippets or error messages

## Feature Requests

For feature requests, please:
- Check if the feature already exists
- Describe the use case clearly
- Explain why the feature would be valuable
- Consider implementation complexity

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional tone

Thank you for contributing!

