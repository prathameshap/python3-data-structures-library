#!/usr/bin/env python3
"""Validates commit messages follow the format: TICKET-ID | description"""

import sys
import re
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

from common import should_skip_validation, print_error, print_warning, print_success, print_info

def validate_commit_message(commit_msg_file):
    """Validate commit message format."""
    
    if should_skip_validation():
        return 0
    
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        commit_msg = f.read().strip()
    
    # Skip merge commits
    if commit_msg.startswith('Merge'):
        print_info('Skipping validation for merge commit')
        return 0
    
    # Skip revert commits
    if commit_msg.startswith('Revert'):
        print_info('Skipping validation for revert commit')
        return 0
    
    # Pattern: TICKET-ID | description
    pattern = r'^[A-Z]+-\d+ \| .+'
    
    if not re.match(pattern, commit_msg):
        print_error('Commit message doesn\'t follow format!\n')
        print('Expected format: <TICKET-ID> | <description>')
        print('Examples:')
        print('  ICOE-34897 | add null check for altImage')
        print('  LA-12345 | fix null pointer in authentication')
        print('  LOGIC-001 | add new workflow for partner sync\n')
        print(f'Your message:\n  {commit_msg}\n')
        print('Please fix and try again.')
        print('\nTo bypass (emergencies only): git commit --no-verify')
        return 1
    
    # Check first line length
    first_line = commit_msg.split('\n')[0]
    if len(first_line) > 100:
        print_warning(f'First line is too long ({len(first_line)} chars, max 100)')
        print('         Consider shortening or adding details on separate lines.\n')
    
    # Check for past tense
    past_tense_pattern = r'\| (added|fixed|updated|changed|removed|deleted|implemented|created)'
    if re.search(past_tense_pattern, commit_msg.lower()):
        print_warning('Use imperative mood (add, fix, update) not past tense (added, fixed, updated)\n')
    
    print_success('Commit message format is valid')
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python validate_commit_msg.py <commit-msg-file>')
        sys.exit(1)
    
    sys.exit(validate_commit_message(sys.argv[1]))