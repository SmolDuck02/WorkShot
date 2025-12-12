# Contributing to WorkShot

First off, thank you for considering contributing to WorkShot! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the behavior you observed and expected**
- **Include your environment details**:
  - OS version (Windows 10/11)
  - Python version
  - WorkShot version

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **Include mockups or examples** if applicable

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the code style** used in the project
3. **Test your changes** thoroughly
4. **Update documentation** if you're changing functionality
5. **Write clear commit messages**
6. **Create a Pull Request** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/workshot.git
cd workshot/WorkShot

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Code Style

- Follow **PEP 8** for Python code
- Use **meaningful variable names**
- Add **comments** for complex logic
- Keep functions **small and focused**
- Write **docstrings** for functions and classes

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add export to PDF functionality

- Implement PDF generation using ReportLab
- Add PDF option to export modal
- Update documentation

Fixes #123
```

## Project Structure

```
WorkShot/
├── tracker/          # Core monitoring logic
├── dashboard/        # Web interface
├── exports/          # Generated exports (gitignored)
├── main.py          # Entry point
└── requirements.txt  # Dependencies
```

## Testing

Currently, WorkShot doesn't have automated tests. We welcome contributions to add:
- Unit tests for core functions
- Integration tests for the monitoring system
- UI tests for the dashboard

## Documentation

- Update the README.md if you change functionality
- Add comments to complex code
- Update inline documentation for API changes

## Community

- Be respectful and constructive
- Help others in issues and discussions
- Share your WorkShot use cases!

## Questions?

Feel free to open an issue with the `question` label or start a discussion.

---

Thank you for contributing! ⚡


