#!/usr/bin/env python3
"""
Script to check for dead links in the DaVinci Codex repository.
This script scans all markdown files for internal and external links,
then verifies if the internal links point to existing files.
"""

import os
import re
import requests
import json
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Set

def find_markdown_files(repo_root: str) -> List[str]:
    """Find all markdown files in the repository, excluding .venv directory."""
    md_files = []
    for root, dirs, files in os.walk(repo_root):
        # Skip .venv directory
        if '.venv' in dirs:
            dirs.remove('.venv')
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    return md_files

def extract_links(file_path: str) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    """
    Extract internal and external links from a markdown file.
    Returns a tuple of (internal_links, external_links) where each link is a tuple of (link_text, line_number).
    """
    internal_links = []
    external_links = []
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue
    
    if lines is None:
        print(f"Warning: Could not decode file {file_path} with any supported encoding")
        return [], []
    
    for line_num, line in enumerate(lines, 1):
        # Match markdown links: [text](url)
        for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line):
            text, url = match.groups()
            
            # Skip anchor links (starting with #)
            if url.startswith('#'):
                continue
                
            # Check if it's an external link
            if url.startswith(('http://', 'https://')):
                external_links.append((url, line_num))
            else:
                internal_links.append((url, line_num))
        
        # Match reference-style links: [text]: url
        for match in re.finditer(r'^\s*\[([^\]]+)\]:\s*(.+)$', line, re.MULTILINE):
            ref, url = match.groups()
            url = url.strip()
            
            # Skip anchor links
            if url.startswith('#'):
                continue
                
            # Check if it's an external link
            if url.startswith(('http://', 'https://')):
                external_links.append((url, line_num))
            else:
                internal_links.append((url, line_num))
    
    return internal_links, external_links

def resolve_internal_path(file_path: str, link: str) -> str:
    """Resolve an internal link relative to the file containing it."""
    # Remove any anchor fragments
    link = link.split('#')[0]
    
    # Get the directory of the file containing the link
    file_dir = os.path.dirname(file_path)
    
    # Join the link path with the file directory
    if link.startswith('/'):
        # Absolute path from repo root
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(repo_root, link.lstrip('/'))
    else:
        # Relative path
        return os.path.abspath(os.path.join(file_dir, link))

def check_internal_link_exists(link_path: str) -> bool:
    """Check if an internal link points to an existing file or directory."""
    # First check if the exact path exists
    if os.path.exists(link_path):
        return True
    
    # If it doesn't exist, try adding .md extension
    if not link_path.endswith('.md') and os.path.exists(link_path + '.md'):
        return True
    
    # If it's a directory, check if there's an index.md inside
    if os.path.isdir(link_path):
        index_path = os.path.join(link_path, 'index.md')
        if os.path.exists(index_path):
            return True
    
    return False

def check_external_link(url: str) -> Tuple[bool, str]:
    """Check if an external link is accessible."""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code < 400, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    markdown_files = find_markdown_files(repo_root)
    
    all_internal_links = []
    all_external_links = []
    dead_internal_links = []
    dead_external_links = []
    
    print(f"Scanning {len(markdown_files)} markdown files...")
    
    # Extract all links
    for md_file in markdown_files:
        relative_path = os.path.relpath(md_file, repo_root)
        internal, external = extract_links(md_file)
        
        for link, line_num in internal:
            resolved_path = resolve_internal_path(md_file, link)
            exists = check_internal_link_exists(resolved_path)
            
            all_internal_links.append({
                'file': relative_path,
                'line': line_num,
                'link': link,
                'resolved_path': os.path.relpath(resolved_path, repo_root),
                'exists': exists
            })
            
            if not exists:
                dead_internal_links.append({
                    'file': relative_path,
                    'line': line_num,
                    'link': link,
                    'resolved_path': os.path.relpath(resolved_path, repo_root)
                })
        
        for link, line_num in external:
            all_external_links.append({
                'file': relative_path,
                'line': line_num,
                'link': link,
                'checked': False
            })
    
    # Print summary
    print(f"\nFound {len(all_internal_links)} internal links and {len(all_external_links)} external links.")
    print(f"Found {len(dead_internal_links)} dead internal links.")
    
    # Print dead internal links
    if dead_internal_links:
        print("\n=== DEAD INTERNAL LINKS ===")
        for link in dead_internal_links:
            print(f"File: {link['file']}:{link['line']}")
            print(f"  Link: {link['link']}")
            print(f"  Resolved path: {link['resolved_path']}")
            
            # Try to suggest a fix
            possible_fix = suggest_fix(link['resolved_path'])
            if possible_fix:
                print(f"  Suggested fix: {possible_fix}")
            print()
    
    # Check a sample of external links (to avoid making too many requests)
    print("\n=== EXTERNAL LINKS (SAMPLE CHECK) ===")
    sample_size = min(10, len(all_external_links))
    checked_count = 0
    
    for i, link in enumerate(all_external_links):
        if checked_count >= sample_size:
            break
            
        print(f"Checking: {link['link']}")
        is_valid, status = check_external_link(link['link'])
        
        if not is_valid:
            dead_external_links.append({
                'file': link['file'],
                'line': link['line'],
                'link': link['link'],
                'error': status
            })
            print(f"  [X] DEAD: {status}")
        else:
            print(f"  [OK]")
        
        checked_count += 1
    
    # Save detailed results to JSON
    results = {
        'summary': {
            'total_files': len(markdown_files),
            'total_internal_links': len(all_internal_links),
            'total_external_links': len(all_external_links),
            'dead_internal_links': len(dead_internal_links),
            'dead_external_links': len(dead_external_links)
        },
        'dead_internal_links': dead_internal_links,
        'dead_external_links': dead_external_links,
        'all_internal_links': all_internal_links,
        'all_external_links': all_external_links
    }
    
    with open('link_check_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to link_check_results.json")
    print(f"Total: {len(dead_internal_links)} dead internal links, {len(dead_external_links)} dead external links (from sample)")

def suggest_fix(path: str) -> str:
    """Try to suggest a fix for a dead link."""
    # Check if adding .md would help
    if not path.endswith('.md') and os.path.exists(path + '.md'):
        return path + '.md'
    
    # Check if there's a similar file in the same directory
    dir_path = os.path.dirname(path)
    filename = os.path.basename(path)
    
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            if filename.lower() in file.lower():
                return os.path.join(dir_path, file)
    
    return None

if __name__ == "__main__":
    main()