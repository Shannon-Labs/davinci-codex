# Dead Links Report for DaVinci Codex Repository

## Summary

This report documents the dead links that were found and subsequently fixed in the DaVinci Codex repository. A full repository scan was performed.

**Status: ✅ ALL ISSUES RESOLVED**

- **Total markdown files scanned**: 90
- **Total internal links found**: 152
- **Total external links found**: 58
- **Dead internal links**: 0
- **Dead external links**: 0 (3 fixed in the latest scan)

## Link Fixes (October 2025)

### 1. Defunct "Universal Leonardo" Project Website ✅ FIXED

**File**: `README.md`
**Link**: `https://www.universalleonardo.org/`
**Issue**: The website for the Universal Leonardo project is no longer active (Name Resolution Error).
**Resolution**: Replaced the dead link with a reference to a book by Martin Kemp, the project's lead, providing a stable, authoritative alternative. The new link is `https://global.oup.com/academic/product/leonardo-9780199583355`.

### 2. GitHub Discussions Page Not Found ✅ FIXED

**File**: `showcase/index.md`
**Link**: `https://github.com/Shannon-Labs/davinci-codex/discussions`
**Issue**: HTTP 404 - GitHub Discussions is not enabled for the repository.
**Resolution**: Updated the link to point to the repository's **Issues** page, which serves as the primary forum for community discussion.

### 3. Broken Link to "Revolving Bridge" Folio ✅ FIXED

**File**: `docs/revolving_bridge.md`
**Link**: `https://www.leonardodigitale.com/opera/ca-855-r/`
**Issue**: HTTP 404 - The page for the specific folio was not found.
**Resolution**: Found an alternative, stable link on `leonardomachines.com` that describes the revolving bridge from the same codex. The new link is `https://www.leonardomachines.com/projects/project-the-wood-bridges/`.

## Previously Identified Issues

The following issues were resolved in a previous maintenance cycle:

- **Missing `ABSTRACT.md` file**: This file was created and linked correctly in `README.md`.
- **`CONTRIBUTING.md` link to Discussions**: This was also updated to point to the Issues page.

## Additional Notes

1.  **Comprehensive External Link Check**: All 58 external links were checked via HTTP requests. The previous limitation of checking only a sample has been removed.
2.  **Image Links**: All image links (PNG files) in the documentation were found to be valid.
3.  **Cross-Reference Links**: All cross-references between documentation files are working correctly.

## Recommendations for Future Maintenance

1.  **Completed Actions**:
    - ✅ Updated the link in `README.md` to a stable alternative for the Universal Leonardo project.
    - ✅ Updated the link in `showcase/index.md` to reference Issues instead of Discussions.
    - ✅ Updated the link in `docs/revolving_bridge.md` to a working source.
    - ✅ Modified the link checking script to perform a comprehensive scan.

2.  **Ongoing Maintenance**:
    - Consider setting up a CI check that runs the link validation script automatically to prevent future link rot.
    - When adding new documentation, ensure all links are tested before merging.
    - For external links, consider using version-specific URLs or archive links (like the Wayback Machine) to improve long-term stability.

3.  **Documentation Improvements**:
    - Add a note in the contribution guidelines about checking links before submitting PRs.
    - Consider using relative paths for all internal links to maintain portability.

## Technical Details

The analysis was performed using a custom Python script (`check_links.py`) that was modified to:
- Scan all markdown files in the repository.
- Extract both internal and external links using regex patterns.
- Resolve internal paths relative to their containing files.
- Check for file existence with fallbacks (e.g., adding `.md` extension).
- Perform HTTP HEAD requests on **all** external links.

For detailed, machine-readable results, see the [`link_check_results.json`](link_check_results.json) file generated during the analysis.