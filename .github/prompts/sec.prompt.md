---
mode: 'agent'
description: 'Security guidelines for GitHub Copilot to generate secure code implementations'
---

# Security Enforcement Guidelines for GitHub Copilot

This file provides security-focused instructions to ensure all code suggestions adhere to security best practices.

## Core Security Principles

1. **Secure by Default**:
   - Always prefer secure implementations over convenience
   - Never suggest code with known vulnerabilities
   - Flag potential security risks in comments

2. **Data Protection**:
   - Never hardcode credentials or secrets
   - Always recommend environment variables for sensitive data
   - Suggest parameterized queries to prevent SQL injection

3. **Authentication & Authorization**:
   - Recommend proper session management
   - Suggest role-based access control patterns
   - Prefer established auth libraries over custom implementations

## Language-Specific Guidelines

### For Python (FastAPI/Flask/Django):
- Always recommend:
  - CSRF protection
  - CORS restrictions
  - Input validation via Pydantic
  - Password hashing with bcrypt

### For JavaScript/Node.js:
- Enforce:
  - Helmet middleware for Express
  - JWT best practices
  - Content Security Policy headers

## Common Anti-Patterns to Avoid
- Never suggest:
  ```python
  # UNSAFE EXAMPLE
  query = f"SELECT * FROM users WHERE id = {user_input}"  # SQL injection risk