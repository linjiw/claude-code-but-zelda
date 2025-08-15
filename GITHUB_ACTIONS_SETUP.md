# 🚀 GitHub Actions Deployment Setup Guide

## ✅ What I've Done For You

1. Created `.github/workflows/static.yml` - GitHub Actions workflow
2. Configured automatic deployment on every push to main branch
3. Set up proper permissions and environment

## 📋 What You Need To Do (2 minutes)

### Step 1: Enable GitHub Pages in Repository Settings

1. **Go to your repository settings:**
   ```
   https://github.com/linjiw/claude-code-but-zelda/settings/pages
   ```

2. **Under "Build and deployment":**
   - **Source:** Select `GitHub Actions` (NOT "Deploy from a branch")
   - That's it! No other configuration needed here.

### Step 2: Push the Workflow to Trigger First Deployment

The workflow file is ready. Now let's push it to GitHub:

```bash
# These commands are ready to copy-paste:
git add .github/workflows/static.yml
git commit -m "ci: Add GitHub Actions workflow for automatic Pages deployment"
git push origin main
```

### Step 3: Monitor the Deployment

1. **Go to Actions tab:**
   ```
   https://github.com/linjiw/claude-code-but-zelda/actions
   ```

2. **You should see:**
   - A workflow run called "Deploy static content to Pages"
   - It will show a yellow dot (running) then green check (success)
   - Takes about 1-2 minutes

3. **Check deployment status:**
   ```
   https://github.com/linjiw/claude-code-but-zelda/deployments
   ```

## 🎯 Your Live Site URL

Once deployed (2-3 minutes), your site will be live at:
```
https://linjiw.github.io/claude-code-but-zelda
```

## ✨ How It Works

The GitHub Actions workflow:
1. **Triggers** on every push to main branch
2. **Uploads** the `/docs` folder as an artifact
3. **Deploys** to GitHub Pages automatically
4. **Updates** your live site in ~1 minute

## 🔍 Verify It's Working

### Success Indicators:
- ✅ Green checkmark on Actions tab
- ✅ "github-pages" environment shows in repo sidebar
- ✅ Site loads at: https://linjiw.github.io/claude-code-but-zelda
- ✅ All sound buttons work when clicked
- ✅ Terminal simulation responds to commands

### If Something Goes Wrong:

1. **Check Actions tab for errors:**
   - Click on the failed workflow
   - Read the error messages
   - Most common: permissions issue (see below)

2. **Permissions Issue Fix:**
   - Go to Settings → Actions → General
   - Scroll to "Workflow permissions"
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"
   - Save

3. **Pages Not Enabled:**
   - Go to Settings → Pages
   - Make sure Source is "GitHub Actions"
   - NOT "Deploy from a branch"

## 🔄 Future Updates

To update your site, just:
1. Edit files in `/docs` folder
2. Commit and push to main branch
3. GitHub Actions automatically redeploys
4. Changes live in ~1 minute

## 📊 Monitoring

- **Actions History:** See all deployments at `/actions`
- **Environments:** Check status at `/deployments`
- **Pages Settings:** Configure at `/settings/pages`

## 🎮 Interactive Features on Your Site

Your GitHub Pages site includes:
- **18+ Sound Buttons** - Click to hear actual Zelda sounds
- **Live Terminal** - Type commands like `npm test`, `@zelda stats`
- **Combo System** - Chain successes for combo sounds
- **Stats Display** - Real-time command tracking
- **Smooth Animations** - Sparkles, ripples, and glow effects
- **Responsive Design** - Works on all devices

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow doesn't run | Push any small change to trigger it |
| 404 error on site | Wait 5 minutes, GitHub Pages takes time |
| Sounds don't play | Check browser allows audio autoplay |
| Actions tab missing | Enable Actions in repo settings |
| Permission denied | Update workflow permissions (see above) |

## 📝 Commands Summary

```bash
# Initial setup (one time)
git add .github/workflows/static.yml
git commit -m "ci: Add GitHub Actions workflow for automatic Pages deployment"
git push origin main

# Future updates (anytime)
git add docs/
git commit -m "Update GitHub Pages site"
git push origin main
```

---

**Ready to deploy!** Follow Step 1 and Step 2 above, and your site will be live in minutes! 🚀