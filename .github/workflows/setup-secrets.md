# Setting Up GitHub Secrets for CI/CD

To enable automated NPM publishing, you need to set up the following secret in your GitHub repository:

## Required Secret: NPM_TOKEN

1. **Get your NPM token:**
   ```bash
   npm login
   npm token create --read-only=false
   ```
   Copy the generated token.

2. **Add to GitHub repository:**
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `NPM_TOKEN`
   - Value: Your NPM token
   - Click "Add secret"

## Optional: Customizing Workflows

The workflows support several customization options:

### Test Workflow
- Runs on: Push to main/develop, Pull Requests
- Matrix: Windows, macOS, Linux × Python 3.8-3.12
- Can be triggered manually with debug logging

### Publish Workflow
- Triggered by: GitHub Release or Manual dispatch
- Supports: Dry run mode for testing
- Version bump: patch, minor, or major

### Verify Install Workflow
- Runs: Weekly (Sundays 2 AM UTC)
- Tests: Real NPM installation across platforms
- Can specify version to test

## Monitoring

Check workflow status at:
https://github.com/linjiw/claude-code-but-zelda/actions

## Badges

Add these to your README:

```markdown
![Tests](https://github.com/linjiw/claude-code-but-zelda/workflows/Cross-Platform%20Tests/badge.svg)
![NPM](https://img.shields.io/npm/v/zelda-claude-code)
![Downloads](https://img.shields.io/npm/dm/zelda-claude-code)
```