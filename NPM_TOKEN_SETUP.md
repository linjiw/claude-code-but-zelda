# 🔐 NPM Token & GitHub Secrets Setup Guide

Follow these steps to set up automated NPM publishing for the Zelda Claude Code project.

## Step 1: Generate NPM Token

### Option A: Using NPM CLI (Recommended)
Open your terminal and run:

```bash
# Make sure you're logged in
npm whoami
# Should show: joewwang

# Create an automation token
npm token create --read-only=false
```

When prompted, enter your NPM password. The output will look like:
```
┌────────────────┬──────────────────────────────────────┐
│ token          │ npm_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx   │
│ cidr_whitelist │                                      │
│ readonly       │ false                                │
│ automation     │ false                                │
│ created        │ 2025-08-18T07:23:45.678Z           │
└────────────────┴──────────────────────────────────────┘
```

**IMPORTANT**: Copy the token value (starts with `npm_`) - you won't be able to see it again!

### Option B: Using NPM Website
1. Go to https://www.npmjs.com/
2. Log in to your account (joewwang)
3. Click your profile picture → Access Tokens
4. Click "Generate New Token"
5. Select "Automation" (for CI/CD)
6. Give it a name like "GitHub Actions - zelda-claude-code"
7. Click "Generate Token"
8. **Copy the token immediately!**

## Step 2: Add Token to GitHub Secrets

1. Go to your repository: https://github.com/linjiw/claude-code-but-zelda

2. Navigate to: **Settings** → **Secrets and variables** → **Actions**

3. Click **"New repository secret"**

4. Fill in:
   - **Name**: `NPM_TOKEN`
   - **Secret**: Paste your NPM token (npm_xxxx...)

5. Click **"Add secret"**

## Step 3: Verify Setup

### Test the Workflow Manually:

1. Go to: https://github.com/linjiw/claude-code-but-zelda/actions

2. Click on **"Publish to NPM"** workflow

3. Click **"Run workflow"** button

4. Select options:
   - Version bump: `patch`
   - Dry run: `true` (for testing)

5. Click **"Run workflow"**

6. Watch the workflow run - it should complete successfully

### Check the Results:
- Green checkmark = Token is working!
- Red X = Check the error logs

## Step 4: Enable Automated Publishing

Once verified, the workflow will automatically:
- Run tests on every PR
- Publish to NPM when you create a GitHub release
- Or manually trigger with version bump

## 🎯 Quick Checklist

- [ ] Generated NPM token
- [ ] Added NPM_TOKEN to GitHub secrets
- [ ] Tested workflow with dry run
- [ ] Workflow shows green checkmark

## 🔒 Security Notes

- **Never commit tokens to code**
- **Tokens expire** - regenerate if needed
- **Use automation tokens** for CI/CD
- **Limit token permissions** when possible

## 🆘 Troubleshooting

### "Incorrect or missing password"
- Your NPM account might have 2FA enabled
- Use website method to generate token

### "401 Unauthorized" in workflow
- Token might be expired or incorrect
- Regenerate token and update secret

### "404 Not Found" in workflow  
- Package name might be taken
- Check package.json name field

## 📊 Monitor Your Package

- NPM Package: https://www.npmjs.com/package/zelda-claude-code
- Downloads: https://npm-stat.com/charts.html?package=zelda-claude-code
- GitHub Actions: https://github.com/linjiw/claude-code-but-zelda/actions

---

Once complete, your CI/CD pipeline will:
✅ Test on Windows, macOS, Linux
✅ Auto-publish on release
✅ Verify installation works
✅ Run weekly compatibility checks