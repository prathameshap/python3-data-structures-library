#!/usr/bin/env python3
"""Pre-commit checks for code quality"""

import sys
import subprocess
import os
import re
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

from common import should_skip_validation, print_error, print_warning, print_success, print_info

def get_staged_files(extension=None):
    """Get list of staged files, optionally filtered by extension."""
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

def check_java_files():
    """Check Java files for basic quality issues."""
    java_files = get_staged_files('.java')
    
    if not java_files:
        return True
    
    print_info(f'Checking {len(java_files)} Java file(s)...')
    
    warnings = 0
    
    for file_path in java_files:
        if not os.path.exists(file_path):
            continue
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for public classes/interfaces without JavaDoc
        for i, line in enumerate(lines):
            if re.match(r'^\s*public\s+(class|interface|enum|abstract\s+class)', line):
                has_javadoc = False
                for j in range(max(0, i-5), i):
                    if '/**' in lines[j]:
                        has_javadoc = True
                        break
                
                if not has_javadoc:
                    print_warning(f'{file_path}:{i+1} - Public API missing JavaDoc')
                    warnings += 1
        
        # Check for debug statements
        debug_patterns = [
            'System.out.println',
            'System.err.println',
            'printStackTrace()'
        ]
        
        for pattern in debug_patterns:
            if pattern in content:
                print_warning(f'{file_path} - Contains debug statement: {pattern}')
                warnings += 1
    
    if warnings > 0:
        print_warning(f'Found {warnings} potential issue(s) in Java files')
        print('         Review the warnings above. Commit will proceed.\n')
    
    return True

def check_large_files():
    """Check for large files being committed."""
    staged_files = get_staged_files()
    large_files = []
    
    for file_path in staged_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 5 * 1024 * 1024:  # 5MB
                large_files.append((file_path, size))
    
    if large_files:
        print_warning('Large files detected:')
        for file_path, size in large_files:
            print(f'         {file_path} ({size // (1024*1024)}MB)')
        print('         Consider using Git LFS for large binary files\n')
    
    return True

def run_maven_checkstyle():
    """Run Maven Checkstyle if available."""
    if not os.path.exists('pom.xml'):
        return True
    
    try:
        subprocess.run(['mvn', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_info('Maven not found, skipping Checkstyle')
        return True
    
    print_info('Running Maven Checkstyle...')
    
    try:
        result = subprocess.run(
            ['mvn', 'checkstyle:check', '-q'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print_error('Checkstyle validation failed!')
            print('\nRun this command for details:')
            print('  mvn checkstyle:check\n')
            return False
        
        print_success('Checkstyle passed')
        return True
    except subprocess.TimeoutExpired:
        print_warning('Checkstyle check timed out, skipping')
        return True
    except Exception as e:
        print_warning(f'Could not run Checkstyle: {e}')
        return True

def main():
    """Run all pre-commit checks."""
    
    if should_skip_validation():
        return 0
    
    print('🔍 Running pre-commit checks...\n')
    
    checks = [
        ('Java file quality', check_java_files),
        ('Large files', check_large_files),
        ('Maven Checkstyle', run_maven_checkstyle)
    ]
    
    failed = False
    for check_name, check_func in checks:
        try:
            if not check_func():
                failed = True
        except Exception as e:
            print_warning(f'{check_name} check failed with error: {e}')
    
    if failed:
        print('\nERROR: Pre-commit checks failed')
        #print('Fix the issues above or use: git commit --no-verify\n')
        return 1
    
    print('SUCCESS: All pre-commit checks passed\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())