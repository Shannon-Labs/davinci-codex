<!-- b797154e-1d7f-4c77-8471-4defa3f78fd7 11d5bfd1-80c3-4a1b-a0f3-32e0921cc3cc -->
# Fix GitHub Repository & Jekyll Site Viewability

## Phase 1: Fix README Image Paths & Links

### 1.1 Audit and Fix Image References

- Review all image paths in `README.md` to ensure they work on both GitHub and locally
- Fix relative paths to use consistent format (e.g., `docs/images/...` or `artifacts/...`)
- Verify all referenced images exist; replace missing ones with available alternatives

### 1.2 Fix Documentation Links

- Update markdown links to work correctly on GitHub Pages (remove `.md` extensions for internal links)
- Ensure all CTAs and navigation links use proper format
- Fix links like `[Technical Drawing]` that are missing the link syntax

### 1.3 Create Missing Asset Mapping Script

Create `scripts/audit_missing_assets.py` to:

- Scan all markdown files for image references
- Check if referenced images exist
- Generate a report of missing assets
- Suggest available alternatives from `artifacts/` and `docs/images/`

## Phase 2: Add Missing Invention Pages

### 2.1 Create Missing Documentation

- `docs/armored_walker.md` - Document the armored walker invention
- `docs/variable_pitch_mechanism.md` - Document the variable pitch mechanism
- Ensure both follow the same structure as existing invention pages

### 2.2 Update Landing Page Inventory

- Add armored walker and variable pitch mechanism to `docs/index.md` in appropriate categories
- Verify all 17 inventions are represented on the site

## Phase 3: Fix Jekyll Site Image Handling

### 3.1 Create Image Fallback System

Update `docs/_layouts/landing.html`:

- Add graceful degradation for missing hero images
- Use placeholder CSS backgrounds or available images as fallbacks
- Add existence checks before rendering image-dependent sections

### 3.2 Map Available Images to Landing Page

- Replace missing hero images with available alternatives:
- Use `docs/images/aerial_screw_performance.png` for aerial screw hero
- Use `docs/images/ornithopter_lift.png` for ornithopter
- Use `docs/images/parachute_descent.png` for parachute
- Use available artifact images for other inventions
- Update `docs/index.md` to reference images that actually exist

### 3.3 Create Missing Critical Assets

For images that can't be substituted:

- Create a simple hero texture background (or use existing `hero-texture.png`)
- Generate placeholder images for critical missing items
- Document what professional images should be created later

## Phase 4: Fix Jekyll Configuration & Baseurl Handling

### 4.1 Audit Template Path References

Review and fix in `docs/_layouts/`:

- Ensure all asset paths use `{{ 'path' | relative_url }}` filter
- Verify CSS and JS loading works with `/davinci-codex` baseurl
- Check that image paths in layouts handle baseurl correctly

### 4.2 Update Jekyll Config

- Verify `_config.yml` baseurl and url settings are correct
- Ensure exclude patterns don't hide necessary files
- Add proper 404 handling

### 4.3 Fix Include Files

Review `docs/_includes/`:

- `hero.html` - ensure it handles missing images gracefully
- `navbar.html` - verify all navigation links work
- `footer.html` - check for broken links
- Update to handle both Jekyll site and GitHub rendering

## Phase 5: Fix GitHub Actions Workflow

### 5.1 Simplify Pages Workflow

Update `.github/workflows/pages.yml`:

- Remove complex simulation generation (too slow for CI)
- Focus on reliable Jekyll build
- Ensure Gemfile dependencies install correctly
- Add better error handling and validation

### 5.2 Fix Build Steps

- Ensure `bundle install` works with current Gemfile
- Verify Jupyter Book integration doesn't break Jekyll
- Add validation that required files exist before deployment
- Fix artifact copying to avoid missing file errors

## Phase 6: Create Asset Management Tools

### 6.1 Create Image Synchronization Script

`scripts/sync_artifacts_to_docs.py`:

- Copy relevant simulation images from `artifacts/*/sim/` to `docs/images/`
- Create thumbnail versions if needed
- Update a manifest of available images

### 6.2 Create Link Validation Script

`scripts/validate_links.py`:

- Check all internal links in markdown files
- Verify image references exist
- Report broken links and missing files
- Suggest fixes

## Phase 7: Testing & Validation

### 7.1 Local Testing

- Build Jekyll site locally: `cd docs && bundle exec jekyll serve`
- Verify all pages render correctly
- Check that images load properly
- Test responsive design

### 7.2 Update Testing Documentation

- Add instructions for testing Jekyll site locally
- Document common issues and solutions
- Create troubleshooting guide for missing assets

## Deliverables

1. Fixed `README.md` with working image paths
2. Missing invention documentation pages
3. Updated landing page with all 17 inventions
4. Gracefully degrading Jekyll site
5. Fixed GitHub Actions workflow
6. Asset management and validation scripts
7. Updated documentation for contributors

### To-dos

- [ ] Audit and fix all image paths in README.md
- [ ] Fix documentation links to work on GitHub Pages
- [ ] Create script to audit missing assets and suggest alternatives
- [ ] Create documentation pages for armored_walker and variable_pitch_mechanism
- [ ] Add all 17 inventions to landing page
- [ ] Map existing images to landing page hero sections and update index.md
- [ ] Add graceful degradation for missing images in landing.html
- [ ] Ensure all Jekyll templates use relative_url filter correctly
- [ ] Update hero.html and other includes to handle missing assets
- [ ] Update GitHub Actions workflow for reliable Jekyll build
- [ ] Create script to sync artifact images to docs
- [ ] Create script to validate all internal links and images
- [ ] Test Jekyll site build locally and verify all pages render