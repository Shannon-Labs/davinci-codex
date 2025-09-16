# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The da Vinci Codex project takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

Please report security vulnerabilities by emailing: security@shannon-labs.com

Include the following in your report:
- Type of issue (e.g., code execution, data exposure, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### What to Expect

- **Response Time**: We will acknowledge your email within 48 hours
- **Resolution Timeline**: We aim to resolve critical issues within 7 days
- **Disclosure**: We follow coordinated disclosure and will work with you on timing

### Security Scope

This project focuses on educational civil engineering inventions. We specifically exclude:
- Weaponizable designs
- Potentially harmful mechanisms
- Dual-use technologies without clear civil applications

### Recognition

We maintain a hall of fame for security researchers who help improve our project:
- Contributors will be acknowledged in our CONTRIBUTORS.md file
- Significant findings may result in public recognition (with your permission)

## Safety by Design

All inventions in this repository undergo:
1. **Ethical Review**: Ensuring civil/educational focus
2. **Failure Analysis**: Documenting potential failure modes
3. **Safety Margins**: Building in appropriate safety factors
4. **Material Verification**: Using proven, safe materials

## Dependencies

We regularly audit our dependencies using:
- GitHub Dependabot alerts
- `pip audit` for Python packages
- CodeQL analysis in CI/CD

## Contact

For general questions about security practices: security@shannon-labs.com
For urgent security issues: Use the email above with [URGENT] in the subject line