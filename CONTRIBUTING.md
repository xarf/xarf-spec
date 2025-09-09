# Contributing to XARF Specification

Thank you for your interest in contributing to the XARF v4 specification! This document provides guidelines for contributing to the eXtended Abuse Reporting Format.

## 🤝 How to Contribute

### Reporting Issues
- **Bug Reports**: Use GitHub Issues for specification errors or inconsistencies
- **Feature Requests**: Propose new abuse classes, fields, or improvements
- **Sample Contributions**: Submit real-world (anonymized) abuse report examples

### Contributing Code/Content
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-abuse-type`)
3. **Make** your changes following our guidelines
4. **Test** your changes (validate JSON samples, check documentation)
5. **Submit** a pull request with a clear description

## 📋 Contribution Guidelines

### Documentation Changes
- Use clear, professional language
- Include examples for new concepts
- Maintain consistency with existing terminology
- Update relevant sections when making changes

### Sample Contributions
- **Anonymize** all real data (IPs, domains, emails, etc.)
- **Validate** against the JSON schema
- **Include** contextual comments explaining the abuse scenario
- **Cover** edge cases and real-world variations

### Schema Changes
- **Backward compatibility** must be maintained where possible
- **Document** breaking changes clearly
- **Provide** migration guidance for implementers
- **Consider** impact on existing parsers

## 🏗️ Development Process

### Pull Request Process
1. **Description**: Clearly describe what changes you're making and why
2. **Testing**: Ensure all samples validate and documentation is accurate
3. **Review**: Address feedback from maintainers and community
4. **Approval**: PRs require approval from at least one maintainer

### Review Criteria
- **Technical accuracy** of abuse reporting concepts
- **Clarity** of documentation and examples
- **Consistency** with existing specification
- **Community value** of the contribution

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- **New abuse types** within existing classes
- **Real-world samples** for testing and validation
- **Translation** of documentation into other languages
- **Integration guides** for security tools and SIEMs

### Medium Priority
- **Documentation improvements** and clarifications
- **JSON schema enhancements** for better validation
- **Best practice guides** for implementers
- **Industry-specific examples** (ISP, hosting, law enforcement)

## 📝 Style Guidelines

### Documentation
- Use **present tense** ("XARF provides" not "XARF will provide")
- Be **specific** rather than vague
- Include **code examples** where helpful
- Use **active voice** when possible

### Sample Data
```json
{
  "comment": "Brief explanation of the abuse scenario",
  "xarf_version": "4.0.0",
  "class": "messaging",
  "type": "spam",
  // ... rest of sample
}
```

### Commit Messages
- Use **imperative mood** ("Add new phishing type" not "Added new phishing type")
- **Limit** first line to 50 characters
- **Reference** issue numbers when applicable
- **Explain** the "why" not just the "what"

## 🔍 Testing Your Changes

Before submitting a PR:

### Documentation Changes
- [ ] Spelling and grammar check
- [ ] Links work correctly
- [ ] Formatting renders properly
- [ ] Examples are accurate

### Sample Contributions
- [ ] JSON validates against schema
- [ ] Data is properly anonymized
- [ ] Comments explain the scenario
- [ ] Follows naming conventions

### Schema Changes
- [ ] Backward compatibility maintained
- [ ] All samples still validate
- [ ] Documentation updated
- [ ] Breaking changes documented

## 💬 Community Guidelines

### Communication
- **Be respectful** and professional
- **Stay on topic** in discussions
- **Help others** learn and contribute
- **Assume good intentions** from contributors

### Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

1. **Read** the [XARF v4 specification](2_XARF_v4_Technical_Specification.md)
2. **Browse** existing [samples](samples/v4/) for examples
3. **Check** [open issues](https://github.com/xarf/xarf-spec/issues) for contribution opportunities
4. **Join** [discussions](https://github.com/xarf/xarf-spec/discussions) to ask questions

## 📞 Getting Help

- **GitHub Discussions**: For questions and brainstorming
- **GitHub Issues**: For specific bugs or feature requests
- **Email**: contact@xarf.org for private matters

## 🏆 Recognition

Contributors will be recognized in:
- Repository contributor lists
- Release notes for significant contributions
- Conference presentations and papers (with permission)

Thank you for helping make XARF the standard for abuse reporting! 🛡️