#!/usr/bin/env python3
"""Validates branch names follow the convention: type/TICKET-ID-description"""

import sys
import re
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

from common import (
    get_current_branch, 
    should_skip_validation, 
    VALID_BRANCH_TYPES,
    print_error, 
    print_success
)

def validate_branch_name():
    """Validate branch name format."""
    
    if should_skip_validation():
        return 0
    
    branch_name = get_current_branch()
    
    if not branch_name:
        print_error('Could not determine current branch')
        return 0
    
    # Pattern: type/TICKET-ID-description
    pattern = r'^(feature|bugfix|hotfix|refactor|test|docs)/[A-Z]+-\d+-[a-z0-9-]+$'
    
    if not re.match(pattern, branch_name):
        print_error('Branch name doesn\'t follow convention!\n')
        print('Expected format: <type>/<TICKET-ID>-<short-description>\n')
        print('Valid types:')
        for branch_type in VALID_BRANCH_TYPES:
            print(f'  • {branch_type:<10} : {get_branch_type_description(branch_type)}')
        print('\nExamples:')
        print('  feature/ICOE-34897-add-default-image')
        print('  feature/LOGIC-123-add-partner-workflow')
        print('  bugfix/LA-12345-fix-null-pointer\n')
        print(f'Your branch: {branch_name}\n')
        print('To rename: git branch -m <type>/<TICKET-ID>-<description>')
        print('\nTo bypass (emergencies only): git push --no-verify')
        return 1
    
    print_success('Branch name is valid')
    return 0

def get_branch_type_description(branch_type):
    """Get description for branch type."""
    descriptions = {
        'feature': 'New features',
        'bugfix': 'Bug fixes',
        'hotfix': 'Critical production fixes',
        'refactor': 'Code refactoring',
        'test': 'Test additions/updates',
        'docs': 'Documentation changes'
    }
    return descriptions.get(branch_type, '')

if __name__ == '__main__':
    sys.exit(validate_branch_name())