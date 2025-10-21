#!/usr/bin/env python3
"""Validates Logic App workflow files"""

import sys
import json
import os
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

from common import should_skip_validation, print_error, print_warning, print_success, print_info

def get_staged_files(extension=None):
    """Get list of staged files."""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')
        files = [f for f in files if f]
        
        if extension:
            files = [f for f in files if f.endswith(extension)]
        
        return files
    except subprocess.CalledProcessError:
        return []

def validate_workflow_json(file_path):
    """Validate workflow.json structure."""
    errors = []
    warnings = []
    
    if not os.path.exists(file_path):
        return errors, warnings
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f'{file_path}: Invalid JSON - {e}')
        return errors, warnings
    
    # Check required properties
    required_props = ['definition', 'kind']
    for prop in required_props:
        if prop not in workflow:
            errors.append(f'{file_path}: Missing required property "{prop}"')
    
    # Validate definition
    if 'definition' in workflow:
        definition = workflow['definition']
        
        if '$schema' not in definition:
            warnings.append(f'{file_path}: Missing $schema in definition')
        
        if 'triggers' not in definition:
            errors.append(f'{file_path}: No triggers defined')
        
        if 'actions' in definition and not definition['actions']:
            warnings.append(f'{file_path}: Workflow has no actions')
        
        # Check for hardcoded secrets
        if 'actions' in definition:
            for action_name, action in definition['actions'].items():
                action_str = json.dumps(action).lower()
                if any(keyword in action_str for keyword in ['password', 'secret', 'apikey', 'token']):
                    warnings.append(f'{file_path}: Action "{action_name}" may contain hardcoded credentials')
    
    return errors, warnings

def validate_connections_json(file_path):
    """Validate connections.json."""
    errors = []
    warnings = []
    
    if not os.path.exists(file_path):
        return errors, warnings
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            connections = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f'{file_path}: Invalid JSON - {e}')
        return errors, warnings
    
    if 'managedApiConnections' in connections:
        for conn_name, conn_config in connections['managedApiConnections'].items():
            if 'api' not in conn_config:
                errors.append(f'{file_path}: Connection "{conn_name}" missing api configuration')
    
    return errors, warnings

def main():
    """Run Logic App validation checks."""
    
    if should_skip_validation():
        return 0
    
    print_info('Running Logic App validation...\n')
    
    all_errors = []
    all_warnings = []
    
    # Validate workflow files
    workflow_files = get_staged_files('workflow.json')
    if workflow_files:
        print_info(f'Validating {len(workflow_files)} workflow file(s)...')
        for file_path in workflow_files:
            errors, warnings = validate_workflow_json(file_path)
            all_errors.extend(errors)
            all_warnings.extend(warnings)
    
    # Validate connections
    connections_files = get_staged_files('connections.json')
    for file_path in connections_files:
        errors, warnings = validate_connections_json(file_path)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Report results
    if all_errors:
        print_error('Logic App validation failed!\n')
        for error in all_errors:
            print(f'  ERROR: {error}')
        print('\nFix the errors above or use: git commit --no-verify\n')
        return 1
    
    if all_warnings:
        print_warning(f'Found {len(all_warnings)} warning(s):\n')
        for warning in all_warnings:
            print(f'  WARNING: {warning}')
        print('\nWarnings do not block commit.\n')
    
    if workflow_files or connections_files:
        print_success('Logic App validation passed')
    
    return 0

if __name__ == '__main__':
    sys.exit(main())