# Contributing to OCR BC ID Classification

Thank you for your interest in contributing to the OCR BC ID Classification project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/OCR_BC-ID-classification.git
cd OCR_BC-ID-classification
```

3. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install pytest pytest-cov flake8  # development dependencies
```

## Development Process

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure they follow our coding standards:
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Follow PEP 8 style guidelines
- Add type hints where appropriate

3. Add tests for new functionality in the `tests/` directory

4. Run tests and linting:
```bash
pytest tests/
flake8 .
```

5. Commit your changes:
```bash
git add .
git commit -m "Description of your changes"
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the requirements.txt if you've added new dependencies
3. Push to your fork and submit a pull request
4. Wait for review and address any feedback

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting PR
- Include both positive and negative test cases
- Use pytest fixtures where appropriate

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small
- Use type hints for better code clarity

## Documentation

When adding new features, please update:
- Function/class docstrings
- README.md if needed
- Comments for complex logic
- API documentation if applicable

## Reporting Issues

When reporting issues, please include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- System information

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## Questions?

If you have questions, feel free to:
- Open an issue
- Ask in pull request comments
- Contact the maintainers

Thank you for contributing! 