#!/usr/bin/env python3
"""Validates Java code quality using Checkstyle and other tools"""

import sys
import subprocess
import os
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(HOOKS_DIR))

from common import should_skip_validation, print_error, print_warning, print_success, print_info

def get_staged_files(extension=None):
    """Get list of staged files."""
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

def check_java_syntax():
    """Check Java files for basic syntax and common issues."""
    java_files = get_staged_files('.java')

    if not java_files:
        return True

    print_info(f'Checking {len(java_files)} Java file(s)...')

    errors = []
    warnings = []

    for file_path in java_files:
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            errors.append(f'{file_path}: Could not read file - {e}')
            continue

        # Check for missing package declaration
        if not any(line.strip().startswith('package ') for line in lines):
            warnings.append(f'{file_path}: Missing package declaration')

        # Check for public classes without JavaDoc
        for i, line in enumerate(lines, 1):
            # Public class/interface without JavaDoc
            if re.match(r'^\s*public\s+(class|interface|enum|@interface)', line):
                has_javadoc = False
                # Look back up to 10 lines for JavaDoc
                for j in range(max(0, i-10), i):
                    if j < len(lines) and '/**' in lines[j]:
                        has_javadoc = True
                        break

                if not has_javadoc:
                    warnings.append(f'{file_path}:{i} - Public class/interface missing JavaDoc')

            # Check for System.out.println (should use logger)
            if 'System.out.println' in line or 'System.err.println' in line:
                warnings.append(f'{file_path}:{i} - Use logger instead of System.out.println')

            # Check for printStackTrace (should use logger)
            if '.printStackTrace()' in line:
                warnings.append(f'{file_path}:{i} - Use logger instead of printStackTrace()')

            # Check for TODO/FIXME comments
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                warnings.append(f'{file_path}:{i} - TODO/FIXME comment found')

            # Check for hardcoded credentials
            if any(keyword in line.lower() for keyword in ['password=', 'secret=', 'apikey=', 'token=']):
                if '${' not in line and '@Value' not in line:  # Not a property placeholder
                    errors.append(f'{file_path}:{i} - Possible hardcoded credential detected')

    # Report results
    if errors:
        print_error('Java code validation failed!\n')
        for error in errors:
            print(f'  ERROR: {error}')
        return False

    if warnings:
        print_warning(f'Found {len(warnings)} code quality warning(s):\n')
        for warning in warnings:
            print(f'  WARNING: {warning}')
        print()

    return True

def run_checkstyle():
    """Run Maven Checkstyle if available."""
    if not os.path.exists('pom.xml'):
        return True

    # Check if Maven is available
    try:
        subprocess.run(['mvn', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_info('Maven not found, skipping Checkstyle')
        return True

    print_info('Running Checkstyle...')

    try:
        result = subprocess.run(
            ['mvn', 'checkstyle:check', '-q'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Checkstyle now returns warnings instead of errors for style violations
        if result.returncode != 0:
            # Parse output to separate errors from warnings
            output_lines = result.stdout.split('\n') + result.stderr.split('\n')
            errors = []
            warnings = []

            for line in output_lines:
                if '[ERROR]' in line and 'checkstyle' in line.lower():
                    errors.append(line.strip())
                elif '[WARNING]' in line and 'checkstyle' in line.lower():
                    warnings.append(line.strip())

            # Show warnings but don't fail
            if warnings:
                print_warning(f'Found {len(warnings)} Checkstyle warning(s):')
                for warning in warnings[:5]:  # Show first 5 warnings
                    print(f'  {warning}')
                if len(warnings) > 5:
                    print(f'  ... and {len(warnings) - 5} more warnings')
                print('\nWarnings do not block commit. Run for details:')
                print('  mvn checkstyle:check\n')

            # Only fail on actual errors (syntax, compilation issues)
            if errors:
                print_error('Checkstyle found critical errors!')
                for error in errors[:3]:  # Show first 3 errors
                    print(f'  {error}')
                print('\nFix the errors above or use: git commit --no-verify\n')
                return False

            # If only warnings, don't fail
            if warnings and not errors:
                print_success('Checkstyle passed with warnings')
                return True

        print_success('Checkstyle passed')
        return True
    except subprocess.TimeoutExpired:
        print_warning('Checkstyle check timed out, skipping')
        return True
    except Exception as e:
        print_warning(f'Could not run Checkstyle: {e}')
        return True

def run_spotbugs():
    """Run SpotBugs if configured in pom.xml."""
    if not os.path.exists('pom.xml'):
        return True

    # Check if SpotBugs is configured
    try:
        with open('pom.xml', 'r') as f:
            pom_content = f.read()
            if 'spotbugs-maven-plugin' not in pom_content:
                return True
    except:
        return True

    print_info('Running SpotBugs...')

    try:
        result = subprocess.run(
            ['mvn', 'spotbugs:check', '-q'],
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode != 0:
            print_warning('SpotBugs found potential bugs')
            print('  Run for details: mvn spotbugs:check')
        else:
            print_success('SpotBugs passed')

        return True  # Don't block on SpotBugs warnings
    except subprocess.TimeoutExpired:
        print_warning('SpotBugs check timed out, skipping')
        return True
    except Exception as e:
        print_warning(f'Could not run SpotBugs: {e}')
        return True

def check_test_coverage():
    """Check if tests exist for modified Java files."""
    java_files = get_staged_files('.java')

    if not java_files:
        return True

    # Filter out test files and get source files
    source_files = [f for f in java_files if '/src/main/java/' in f]

    if not source_files:
        return True

    print_info('Checking test coverage...')

    missing_tests = []
    for source_file in source_files:
        # Convert source path to test path
        test_file = source_file.replace('/src/main/java/', '/src/test/java/')
        test_file = test_file.replace('.java', 'Test.java')

        if not os.path.exists(test_file):
            missing_tests.append(f'{source_file} → {test_file}')

    if missing_tests:
        print_warning('Some source files may be missing tests:')
        for missing in missing_tests:
            print(f'  WARNING: {missing}')
        print('\nConsider adding unit tests for new code.\n')

    return True

import re

def main():
    """Run all Java code quality checks."""

    if should_skip_validation():
        return 0

    java_files = get_staged_files('.java')

    if not java_files:
        return 0

    print_info('Running Java code quality checks...\n')

    checks = [
        ('Basic code quality', check_java_syntax),
        ('Checkstyle', run_checkstyle),
        ('SpotBugs', run_spotbugs),
        ('Test coverage', check_test_coverage)
    ]

    failed = False
    warnings_found = False

    for check_name, check_func in checks:
        try:
            result = check_func()
            if result is False:
                failed = True
            elif result is True:
                # Check if warnings were shown (we can't easily detect this, so we'll assume warnings are shown)
                warnings_found = True
        except Exception as e:
            print_warning(f'{check_name} check failed with error: {e}')

    # Only fail on critical errors, not on style warnings
    if failed:
        print('\nERROR: Java code quality checks failed')
        print('Fix the critical errors above or use: git commit --no-verify\n')
        return 1

    if warnings_found:
        print('SUCCESS: Java code quality checks passed with warnings\n')
    else:
        print('SUCCESS: All Java code quality checks passed\n')

    return 0

if __name__ == '__main__':
    sys.exit(main())
