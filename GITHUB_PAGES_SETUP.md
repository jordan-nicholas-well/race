# 🚀 GitHub Pages Deployment Guide

## Quick Setup

1. **Push your code** to GitHub (main or master branch)
2. **Enable GitHub Pages**:
   - Go to Repository Settings → Pages
   - Set Source to "GitHub Actions"
   - Save settings
3. **Automatic deployment** will trigger on the next push

## How It Works

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:

1. ✅ **Installs Python 3.12** and dependencies
2. ✅ **Builds the web version** using Pygbag
3. ✅ **Creates deployment files** in the correct structure
4. ✅ **Deploys to GitHub Pages** on every push to main/master

## Accessing Your Game

After successful deployment, your racing game will be live at:

```
https://[your-username].github.io/[repository-name]/
```

Example: `https://jordan.github.io/race/`

## Troubleshooting

### If deployment fails:

1. **Check the Actions tab** in your GitHub repository for error logs
2. **Verify GitHub Pages is enabled** with "GitHub Actions" source
3. **Ensure all files are committed** (especially `main.py`, `dev.py`, assets)

### Common issues:

- **Missing dependencies**: The workflow installs pygame and pygbag automatically
- **Build errors**: Check that `python dev.py build` works locally first
- **Asset loading**: All PNG files and game assets are included in the build

### Manual verification:

Test locally before pushing:

```bash
# Test the build process
python dev.py build

# Test the web version
python dev.py serve
```

## Deployment Status

Check your deployment status at:

- **Actions tab**: See build/deploy progress
- **Settings → Pages**: View deployment URL and status
- **Repository**: Green checkmark ✅ indicates successful deployment

## Customization

You can customize the deployment by editing `.github/workflows/deploy.yml`:

- **Change Python version**: Modify `python-version`
- **Add build steps**: Include asset generation or optimization
- **Custom domain**: Add CNAME file for custom domains
- **Build triggers**: Modify `on:` section for different trigger conditions

Your racing game is now ready for automatic web deployment! 🎮🌐
