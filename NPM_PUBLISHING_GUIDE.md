# 📦 Complete NPM Publishing Guide for Zelda Claude Code

## Step 1: Create NPM Account (if you don't have one)

### Option A: Via Website
1. Go to https://www.npmjs.com/signup
2. Fill in:
   - **Username**: Choose something unique (e.g., `linjiw`)
   - **Email**: Your email address
   - **Password**: Strong password
3. Verify your email address

### Option B: Via Terminal (Recommended)
```bash
npm adduser
```
This will prompt you for:
- Username
- Password  
- Email
- One-time password (if 2FA enabled)

## Step 2: Login to NPM

Run this command in your terminal:
```bash
npm login
```

Enter your credentials when prompted:
- Username: [your npm username]
- Password: [your password]
- Email: [your email]
- One-time code: [if you have 2FA enabled]

To verify you're logged in:
```bash
npm whoami
```

## Step 3: Final Pre-Publishing Checks

### Test the package locally one more time:
```bash
# Clean install
rm -rf node_modules
npm install

# Test the CLI
npm link
zelda-claude --version
zelda-claude play success
```

### Check what will be published:
```bash
npm pack --dry-run
```
This shows all files that will be included in your package.

### Verify package size:
```bash
npm pack
ls -lh *.tgz
```
The package should be under 10MB ideally.

## Step 4: Publish to NPM

### First Publication:
```bash
npm publish
```

If successful, you'll see:
```
+ zelda-claude-code@2.1.0
```

### If the name is taken, you can:
1. Use a scoped package:
```bash
# Update package.json name to "@linjiw/zelda-claude-code"
npm publish --access public
```

2. Or choose a different name:
```bash
# Update package.json name to something unique
npm publish
```

## Step 5: Verify Publication

1. **Check on NPM website:**
   - Go to: https://www.npmjs.com/package/zelda-claude-code
   - You should see your package!

2. **Test installation:**
```bash
# In a different directory
npm install -g zelda-claude-code
zelda-claude --version
```

## Step 6: Post-Publishing Tasks

### Update your GitHub README:
Add an npm badge:
```markdown
[![npm version](https://badge.fury.io/js/zelda-claude-code.svg)](https://www.npmjs.com/package/zelda-claude-code)
```

### Add installation instructions:
```markdown
## Installation
```bash
npm install -g zelda-claude-code
```
```

### Tag your release on GitHub:
```bash
git tag v2.1.0
git push origin v2.1.0
```

## 📝 Important Notes

### Package Name Availability:
- ✅ `zelda-claude-code` appears to be available
- If taken, use `@linjiw/zelda-claude-code` (scoped package)

### Version Management:
- Current version: 2.1.0
- To update: Change version in package.json, then `npm publish`
- Follow semantic versioning: MAJOR.MINOR.PATCH

### Security:
- Never commit `.npmrc` with auth tokens
- Use 2FA on your npm account (recommended)
- Be careful with `npm publish` - it's permanent!

## 🚀 Quick Publishing Commands

```bash
# 1. Login (first time only)
npm login

# 2. Final test
npm pack --dry-run

# 3. Publish!
npm publish

# 4. Verify
npm info zelda-claude-code
```

## 🆘 Troubleshooting

### "You need to be logged in"
```bash
npm login
```

### "Package name too similar to existing packages"
Use a scoped package:
```bash
# Change name in package.json to "@linjiw/zelda-claude-code"
npm publish --access public
```

### "Cannot publish over previously published version"
Bump the version in package.json:
```json
"version": "2.1.1"
```

### "E403 Forbidden"
- Check if name is taken: `npm view zelda-claude-code`
- Try scoped package: `@username/package-name`

## 📊 After Publishing

Your package will be available at:
- NPM: https://www.npmjs.com/package/zelda-claude-code
- Install: `npm install -g zelda-claude-code`
- Stats: https://npm-stat.com/charts.html?package=zelda-claude-code

## 🎉 Success Checklist

- [ ] Created npm account
- [ ] Logged in with `npm login`
- [ ] Tested package locally
- [ ] Published with `npm publish`
- [ ] Verified on npmjs.com
- [ ] Updated GitHub README
- [ ] Tagged release on GitHub

Good luck with your first npm package! 🚀