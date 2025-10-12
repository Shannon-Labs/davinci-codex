# Site Maintenance Quick Reference

Quick commands and workflows for maintaining the da Vinci Codex Jekyll site.

## Daily Operations

### Sync New Simulation Images
When new simulations are generated:
```bash
python scripts/sync_artifacts_to_docs.py
```

### Validate Links
Before committing documentation changes:
```bash
python scripts/validate_links.py
```

### Check for Missing Assets
```bash
python scripts/audit_missing_assets.py
```

## Adding New Content

### Add a New Invention

1. **Create documentation page:**
   ```bash
   touch docs/<invention_name>.md
   ```

2. **Use this template:**
   ```markdown
   ---
   layout: default
   title: Invention Name
   nav_order: X
   ---
   
   # Invention Name
   **Subtitle**
   
   ## Overview
   ...
   
   ## Source Manuscripts
   ...
   
   ## Available Resources
   - 📊 [Simulation Results](../artifacts/<invention>/sim/)
   - 🔧 [Source Code](../src/davinci_codex/inventions/<invention>.py)
   ```

3. **Add to landing page** (`docs/index.md`):
   ```yaml
   - name: "Invention Name"
     status: "in_progress"
     achievement: "Key achievement"
     description: "Brief description"
     image: "images/<invention>_<image>.png"
     href: "<invention>.html"
     stats:
       - "Stat 1"
       - "Stat 2"
   ```

4. **Sync images if needed:**
   ```bash
   python scripts/sync_artifacts_to_docs.py
   ```

5. **Validate:**
   ```bash
   python scripts/validate_links.py
   cd docs && bundle exec jekyll build
   ```

### Add New Images

**Option 1: Add to docs/images/**
```bash
cp /path/to/image.png docs/images/
```

**Option 2: Generate in artifacts and sync:**
```bash
# Generate simulation with image output to artifacts/<invention>/sim/
python scripts/sync_artifacts_to_docs.py
```

### Update Site Styles

1. Edit CSS: `docs/assets/css/<file>.css`
2. Test locally:
   ```bash
   cd docs
   bundle exec jekyll serve --watch
   ```
3. Verify at `http://localhost:4000/davinci-codex/`

## Testing Workflows

### Quick Local Test
```bash
cd docs
bundle exec jekyll serve --baseurl "/davinci-codex"
# Visit http://localhost:4000/davinci-codex/
```

### Full Build Test
```bash
cd docs
rm -rf _site .jekyll-cache
bundle exec jekyll build --baseurl "/davinci-codex"
```

### Pre-commit Checklist
```bash
# 1. Sync images
python scripts/sync_artifacts_to_docs.py

# 2. Validate links
python scripts/validate_links.py

# 3. Test build
cd docs && bundle exec jekyll build --baseurl "/davinci-codex"

# 4. Check for errors
echo "Build successful! Ready to commit."
```

## Deployment

### Push to GitHub
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### Monitor Deployment
1. Go to GitHub Actions: https://github.com/Shannon-Labs/davinci-codex/actions
2. Watch the "Deploy Professional GitHub Pages" workflow
3. Check for green checkmark ✅
4. Visit: https://shannon-labs.github.io/davinci-codex/

### If Deployment Fails

1. **Check Actions log** for error messages
2. **Common fixes:**
   ```bash
   # Rebuild locally first
   cd docs
   rm -rf _site vendor .jekyll-cache
   bundle install --path vendor/bundle
   bundle exec jekyll build --baseurl "/davinci-codex"
   ```
3. **Verify all images exist:**
   ```bash
   python scripts/audit_missing_assets.py
   ```

## Troubleshooting

### "Bundle install fails"
```bash
cd docs
bundle install --path vendor/bundle
```

### "Jekyll command not found"
```bash
bundle exec jekyll <command>
```

### "Images not loading"
```bash
python scripts/sync_artifacts_to_docs.py
cd docs
bundle exec jekyll build --baseurl "/davinci-codex"
```

### "CSS not applying"
```bash
cd docs
rm -rf _site .jekyll-cache .sass-cache
bundle exec jekyll build --baseurl "/davinci-codex"
```

### "Links broken"
```bash
python scripts/validate_links.py
# Fix reported issues, then rebuild
```

## Backup & Recovery

### Backup Current Site
```bash
cp -r docs/_site docs/_site.backup.$(date +%Y%m%d)
```

### Restore from Git
```bash
git checkout -- docs/
```

### Clean Slate
```bash
cd docs
rm -rf _site .jekyll-cache .sass-cache vendor
bundle install --path vendor/bundle
bundle exec jekyll build --baseurl "/davinci-codex"
```

## Performance

### Check Build Time
```bash
time bundle exec jekyll build --baseurl "/davinci-codex"
```
Target: < 10 seconds

### Check Site Size
```bash
du -sh docs/_site
```
Target: < 50MB

### Optimize Images
```bash
# Install imagemagick if not available
# brew install imagemagick

# Optimize all PNGs
find docs/images -name "*.png" -exec convert {} -strip -quality 85 {} \;
```

## Monitoring

### Check Live Site
```bash
curl -I https://shannon-labs.github.io/davinci-codex/
# Should return 200 OK
```

### Validate HTML
```bash
# Install html5validator
# pip install html5validator

cd docs/_site
html5validator --root . --also-check-css
```

## Resources

- [Full Testing Guide](TESTING.md)
- [Site Improvements Summary](../SITE_IMPROVEMENTS.md)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

---

*Keep this guide updated as new workflows are established!*

