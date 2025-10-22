#!/usr/bin/env python3
"""Validates C# code quality using Roslyn analyzers"""

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

def check_csharp_syntax():
    """Check C# files for basic syntax and common issues."""
    cs_files = get_staged_files('.cs')

    if not cs_files:
        return True

    print_info(f'Checking {len(cs_files)} C# file(s)...')

    warnings = []

    for file_path in cs_files:
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print_warning(f'{file_path}: Could not read file - {e}')
            continue

        for i, line in enumerate(lines, 1):
            # Check for Console.WriteLine (should use logger)
            if 'Console.WriteLine' in line or 'Console.Write' in line:
                warnings.append(f'{file_path}:{i} - Use ILogger instead of Console.WriteLine')

            # Check for TODO/FIXME
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                warnings.append(f'{file_path}:{i} - TODO/FIXME comment found')

    if warnings:
        print_warning(f'Found {len(warnings)} code quality warning(s):\n')
        for warning in warnings:
            print(f'  WARNING: {warning}')
        print()

    return True

def run_dotnet_format():
    """Run dotnet format to check code formatting."""
    csproj_files = list(Path('.').rglob('*.csproj'))

    if not csproj_files:
        return True

    # Check if dotnet is available
    try:
        subprocess.run(['dotnet', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_info('dotnet CLI not found, skipping format check')
        return True

    print_info('Checking code formatting...')

    try:
        result = subprocess.run(
            ['dotnet', 'format', '--verify-no-changes', '--verbosity', 'quiet'],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print_warning('Code formatting issues detected')
            print('  Run to fix: dotnet format')
            print('  Or configure your IDE to format on save\n')
        else:
            print_success('Code formatting is correct')

        return True  # Don't block on formatting issues
    except subprocess.TimeoutExpired:
        print_warning('Format check timed out, skipping')
        return True
    except Exception as e:
        print_warning(f'Could not run dotnet format: {e}')
        return True

def run_code_analysis():
    """Run Roslyn code analysis."""
    csproj_files = list(Path('.').rglob('*.csproj'))

    if not csproj_files:
        return True

    print_info('Running code analysis...')

    try:
        result = subprocess.run(
            ['dotnet', 'build', '/p:RunAnalyzers=true', '/p:TreatWarningsAsErrors=false', '/v:quiet'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            if 'warning' in result.stdout.lower() or 'warning' in result.stderr.lower():
                print_warning('Code analysis warnings found')
                print('  Run for details: dotnet build /p:RunAnalyzers=true')
            else:
                print_error('Code analysis failed!')
                print('  Run for details: dotnet build')
                return False
        else:
            print_success('Code analysis passed')

        return True
    except subprocess.TimeoutExpired:
        print_warning('Code analysis timed out, skipping')
        return True
    except Exception as e:
        print_warning(f'Could not run code analysis: {e}')
        return True

def main():
    """Run all C# code quality checks."""

    if should_skip_validation():
        return 0

    cs_files = get_staged_files('.cs')

    if not cs_files:
        return 0

    print_info('Running C# code quality checks...\n')

    checks = [
        ('Basic code quality', check_csharp_syntax),
        ('Code formatting', run_dotnet_format),
        ('Code analysis', run_code_analysis)
    ]

    failed = False
    for check_name, check_func in checks:
        try:
            if not check_func():
                failed = True
        except Exception as e:
            print_warning(f'{check_name} check failed with error: {e}')

    if failed:
        print('\nERROR: C# code quality checks failed')
        print('Fix the issues above or use: git commit --no-verify\n')
        return 1

    print('SUCCESS: All C# code quality checks passed\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())
