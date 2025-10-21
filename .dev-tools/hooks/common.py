#!/usr/bin/env python3
"""Common utilities for git hooks"""

import subprocess
import sys

# Configuration
PROTECTED_BRANCHES = ['release', 'master'] # protected branches that should not be validated
SKIP_BRANCHES = ['release', 'main', 'master'] # branches that should not be validated
VALID_BRANCH_TYPES = ['feature', 'bugfix', 'hotfix', 'refactor', 'test', 'docs']

def get_current_branch():
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'symbolic-ref', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def should_skip_validation():
    """Check if validation should be skipped for current branch."""
    branch = get_current_branch()
    
    if not branch:
        return True
    
    if branch in SKIP_BRANCHES:
        print(f'INFO: Skipping validation for {branch} branch')
        return True
    
    return False

def print_error(message):
    """Print error message."""
    print(f'ERROR: {message}', file=sys.stderr)

def print_warning(message):
    """Print warning message."""
    print(f'WARNING: {message}')

def print_success(message):
    """Print success message."""
    print(f'SUCCESS: {message}')

def print_info(message):
    """Print info message."""
    print(f'INFO: {message}')