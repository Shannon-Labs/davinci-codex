# Testing the Jekyll Site Locally

This guide explains how to test the da Vinci Codex Jekyll site on your local machine before deploying.

## Prerequisites

- Ruby (2.7 or higher)
- Bundler (`gem install bundler`)
- Git

## Quick Start

### 1. Install Dependencies

```bash
cd docs
bundle install --path vendor/bundle
```

This installs all Jekyll dependencies locally in the `vendor/bundle` directory.

### 2. Build the Site

```bash
bundle exec jekyll build --baseurl "/davinci-codex"
```

This builds the site into the `_site` directory with the correct baseurl for GitHub Pages.

### 3. Serve Locally

```bash
bundle exec jekyll serve --baseurl "/davinci-codex"
```

The site will be available at `http://localhost:4000/davinci-codex/`

### 4. Watch Mode (Auto-rebuild)

```bash
bundle exec jekyll serve --watch --baseurl "/davinci-codex"
```

The site will automatically rebuild when you make changes to files.

## Verification Checklist

Before committing changes, verify:

### Images
- [ ] All images load correctly
- [ ] No broken image links
- [ ] Images have appropriate alt text
- [ ] Image file sizes are reasonable (<500KB for photos)

### Links
- [ ] All internal links work
- [ ] Navigation menu functions correctly
- [ ] External links open in new tabs (if appropriate)

### Layout
- [ ] Site displays correctly on desktop
- [ ] Site is responsive on mobile/tablet
- [ ] No layout overflow issues
- [ ] CSS loads properly

### Content
- [ ] All invention pages render correctly
- [ ] Markdown formatting is correct
- [ ] Code blocks display with syntax highlighting
- [ ] Tables format properly

## Common Issues

### Issue: Bundle install fails with permissions error

**Solution:**
```bash
bundle install --path vendor/bundle
```

This installs gems locally instead of system-wide.

### Issue: Jekyll command not found

**Solution:**
```bash
bundle exec jekyll <command>
```

Always prefix Jekyll commands with `bundle exec`.

### Issue: Images don't load

**Solution:**
Run the image sync script:
```bash
cd ..  # Back to repo root
python scripts/sync_artifacts_to_docs.py
cd docs
```

### Issue: CSS/JS not loading

**Solution:**
Check that baseurl is set correctly:
```bash
bundle exec jekyll serve --baseurl "/davinci-codex"
```

### Issue: Changes not reflecting

**Solution:**
1. Stop the server (Ctrl+C)
2. Clear the cache: `rm -rf _site .jekyll-cache`
3. Rebuild: `bundle exec jekyll serve --watch`

## Automated Checks

Run automated validation scripts:

### Check for Missing Assets
```bash
cd ..  # Back to repo root
python scripts/audit_missing_assets.py
```

### Validate Internal Links
```bash
python scripts/validate_links.py
```

### Sync Artifact Images
```bash
python scripts/sync_artifacts_to_docs.py
```

## Deployment Testing

To test as close to production as possible:

1. Build the site exactly as GitHub Pages will:
   ```bash
   bundle exec jekyll build --baseurl "/davinci-codex"
   ```

2. Serve the built site with a simple HTTP server:
   ```bash
   cd _site
   python -m http.server 8000
   ```

3. Visit `http://localhost:8000` to test

## Performance Testing

### Check Build Time
```bash
time bundle exec jekyll build --baseurl "/davinci-codex"
```

Target: < 10 seconds

### Check Site Size
```bash
du -sh _site
```

Target: < 50MB

### Count Assets
```bash
find _site -type f | wc -l  # Total files
find _site -name "*.png" | wc -l  # Images
find _site -name "*.html" | wc -l  # Pages
```

## Troubleshooting

### Clean Rebuild
```bash
rm -rf _site .jekyll-cache .sass-cache
bundle exec jekyll build --baseurl "/davinci-codex"
```

### Update Dependencies
```bash
bundle update
```

### Check Jekyll Configuration
```bash
bundle exec jekyll doctor
```

## Documentation Updates

When adding new content:

1. **New Invention Page:**
   - Create `docs/<invention>.md`
   - Add front matter with layout, title, nav_order
   - Add to `docs/index.md` in appropriate category
   - Run link validator

2. **New Images:**
   - Add to `docs/images/`
   - Or add to `artifacts/<invention>/sim/` and run sync script
   - Optimize images (use PNG for screenshots, JPEG for photos)
   - Keep file sizes reasonable

3. **New CSS/JS:**
   - Add to `docs/assets/css/` or `docs/assets/js/`
   - Reference in `_layouts/default.html` or `_layouts/landing.html`
   - Test on multiple browsers

## Browser Testing

Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/pages.yml`) automatically:
1. Syncs artifact images
2. Builds Jupyter Book (if available)
3. Builds Jekyll site
4. Deploys to GitHub Pages

Test the workflow locally before pushing:
```bash
# Sync images
python scripts/sync_artifacts_to_docs.py

# Build site
cd docs
bundle exec jekyll build --baseurl "/davinci-codex"
```

## Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)

---

*For issues or questions, open an issue on GitHub or check the [troubleshooting guide](../README.md).*

