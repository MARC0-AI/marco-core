# MARCO Security Principles

MARCO is designed to interact with operating systems, applications, files, services, and external accounts. Security is therefore a core product requirement.

## Principles

### Least privilege

MARCO should only receive the permissions required for the current task.

### Explicit approval

High-risk actions require explicit user approval.

Examples include:

- deleting important files
- sending external communications
- changing security settings
- deploying production systems
- financial transactions

### No secrets in source control

API keys, passwords, tokens, private keys, and credentials must never be committed to Git.

### Auditability

Important actions should produce structured records containing enough information to understand what happened.

### Fail safely

If permission, execution, verification, or communication fails, MARCO should stop rather than silently continue.

### Human control

The user remains the final authority over sensitive actions.

## Reporting

Security vulnerabilities should not be publicly disclosed before they have been responsibly investigated and addressed.
