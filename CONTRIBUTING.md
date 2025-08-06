# Contributing to Crypto Currency Price Tracker

🎉 Thank you for considering contributing to our cryptocurrency price tracking application! This document provides guidelines for contributing to this open-source project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs
- Check existing issues first
- Use the bug report template
- Include system information and steps to reproduce
- Attach screenshots for UI issues

### 💡 Suggesting Features
- Check if the feature has already been requested
- Use the feature request template
- Explain the use case and benefits
- Consider implementation complexity

### 🛠️ Code Contributions
- Fix bugs or implement features
- Improve documentation
- Add tests
- Optimize performance
- Enhance UI/UX

### 📝 Documentation
- Improve README files
- Add code comments
- Create tutorials or guides
- Update API documentation

## 🏗️ Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- Basic knowledge of PyQt5 and cryptocurrency APIs

### Setting Up Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/crypto-tracker.git
   cd crypto-tracker
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv crypto_env
   source crypto_env/bin/activate  # On Windows: crypto_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller  # For building binaries
   ```

4. **Run the Application**
   ```bash
   python crypto_gui.py
   ```

5. **Test Your Setup**
   - Verify all tabs load correctly
   - Test API connectivity
   - Check chart functionality

## 🔄 Development Workflow

### Branch Strategy
- `main`: Stable releases
- `develop`: Development integration
- `feature/feature-name`: New features
- `bugfix/issue-number`: Bug fixes
- `hotfix/critical-fix`: Critical fixes

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow coding standards
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Run the application
   python crypto_gui.py
   
   # Test binary building (if applicable)
   ./build_binary.sh
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

## 📏 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise

### UI/UX Guidelines
- Maintain consistent styling with existing theme
- Use appropriate icons and colors
- Ensure responsive design
- Test on different screen sizes

### Code Organization
```
crypto_gui.py           # Main application file
├── CryptoPriceWidget   # Main widget class
├── setup_ui()         # UI initialization  
├── setup_*_tab()      # Individual tab setup
├── API methods        # Data fetching
└── Analysis methods   # Market analysis logic
```

### Commit Message Convention
```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting, no code change
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance tasks

Examples:
- feat(ui): add dark theme toggle
- fix(api): handle network timeout errors
- docs(readme): update installation instructions
```

## 📤 Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Add comments for complex code
   - Update requirements.txt if needed

2. **Create Pull Request**
   - Use descriptive title
   - Fill out the PR template
   - Link related issues
   - Add screenshots for UI changes

3. **PR Requirements**
   - [ ] Code follows project standards
   - [ ] Changes are tested
   - [ ] Documentation is updated
   - [ ] No merge conflicts
   - [ ] Binary builds successfully (if applicable)

### Review Process
- Maintainers will review your PR
- Address feedback promptly  
- Be open to suggestions
- PR will be merged after approval

## 🐛 Bug Reports

When filing a bug report, please include:

**Environment Information:**
- OS and version
- Python version
- Application version
- Installation method (source/binary)

**Bug Description:**
- Clear title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs

**Template:**
```markdown
**Bug Summary:** Brief description

**Steps to Reproduce:**
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior:** What should happen

**Screenshots:** If applicable

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.9.0]
- Installation: [source/binary]
```

## 💡 Feature Requests

**Template:**
```markdown
**Feature Summary:** Brief description

**Use Case:** Why is this needed?

**Proposed Solution:** How should it work?

**Alternatives Considered:** Other approaches

**Additional Context:** Screenshots, mockups
```

## 🏷️ Areas for Contribution

### High Priority
- [ ] Add more cryptocurrency exchanges
- [ ] Implement portfolio tracking
- [ ] Add price alerts/notifications
- [ ] Mobile responsive design
- [ ] Performance optimizations

### Medium Priority  
- [ ] Additional chart indicators
- [ ] Export functionality (CSV/PDF)
- [ ] Theme customization
- [ ] Multiple language support
- [ ] Unit tests

### Low Priority
- [ ] Plugin system
- [ ] Advanced analysis tools
- [ ] Social features
- [ ] Cloud sync

## 🎯 Development Tips

### Working with APIs
- Handle rate limits gracefully
- Implement proper error handling
- Cache responses when appropriate
- Test with different network conditions

### UI Development
- Use Qt Designer for complex layouts
- Test with different DPI settings
- Ensure keyboard navigation works
- Consider accessibility features

### Performance
- Profile code for bottlenecks
- Optimize API calls
- Minimize resource usage
- Test with large datasets

## 📞 Getting Help

- **Issues**: Create GitHub issue for bugs/questions
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact maintainers for sensitive issues

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Special thanks in documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Happy Contributing! 🚀**

*Help us make the best open-source cryptocurrency tracking application!*
