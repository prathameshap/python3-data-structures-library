# Development Tools

**DO NOT MODIFY FILES IN THIS DIRECTORY** - Managed by DevOps

## Quick Setup

### Step 1: Install Git Hooks

**Windows:**
```cmd
.dev-tools\setup\setup-hooks.bat
```

**Mac/Linux:**
```bash
chmod +x .dev-tools/setup/setup-hooks.sh
.dev-tools/setup/setup-hooks.sh
```

### Step 2: Install Logic Apps Tools (Optional)

**Windows:**
```powershell
.\.dev-tools\setup\setup-logic-apps.ps1
```

**Mac/Linux:**
```bash
chmod +x .dev-tools/setup/setup-logic-apps.sh
.dev-tools/setup/setup-logic-apps.sh
```

---

## What Gets Installed

### Git Hooks

1. **commit-msg** - Validates: `TICKET-ID | description`
2. **pre-commit** - Validates Logic App JSON files
3. **pre-push** - Validates: `type/TICKET-ID-description`

### Logic Apps Tools (Optional)

1. Azure Functions Core Tools v3
2. Azurite (local storage emulator)
3. Node.js verification
4. .NET Core SDK verification

---

## Verification
```bash
# Test commit message
git commit --allow-empty -m "TEST-123 | test message"
# Expected: SUCCESS: Commit message format is valid

# Test branch name
git checkout -b feature/TEST-123-test-branch
# Expected: SUCCESS: Branch name is valid
```

---

## Hooks Behavior

|   Branch    | Hooks Active? |            Reason                    |
|-------------|---------------|--------------------------------------|
| dev         |    Yes        | Enforce standards during development |
| feature/*   |    Yes        | Validate all feature work            |
| bugfix/*    |    Yes        | Validate all bug fixes               |
| hotfix/*    |    Yes        | Validate all hotfixes                |
| refactor/*  |    Yes        | Validate all refactoring             |
| test/*      |    Yes        | Validate all test changes            |
| docs/*      |    Yes        | Validate all documentation changes   |
| **release** |    No         | Don't block release merges           |
| **main**    |    No         | Don't block production deploys       |
| **master**  |    No         | Don't block production deploys       |

**Why skip on release/master?**
- These are protected branches for production deployment
- Hooks running on feature/dev branches already validated the code
- Avoids blocking critical releases

---

## What Gets Validated

### Commit Message Format

**Required:** `TICKET-ID | description`

**Valid Examples:**
```
ICOE-34897 | add null check for altImage
LA-12345 | fix authentication timeout
LOGIC-001 | add new workflow for partner sync
TECH-999 | refactor error handling
```

**Invalid Examples:**
```
fixed bug                   # Missing ticket ID
ICOE-34897 fixed stuff      # Missing pipe |
added new feature           # Past tense
update code                 # No ticket ID
```

**Rules:**
- Must start with uppercase ticket ID (e.g., ICOE-123, LA-456)
- Must have space, pipe `|`, space
- Description should be imperative mood (add, fix, update)
- First line should be under 100 characters
- No past tense (added, fixed, updated)

### Branch Naming Convention

**Required:** `type/TICKET-ID-description`

**Valid Types:**
- `feature/` - New features
- `bugfix/` - Bug fixes  (This is for prod bugs since we do not create new branches for dev bugs)
- `hotfix/` - Critical production fixes
- `refactor/` - Code refactoring
- `test/` - Test additions/updates
- `docs/` - Documentation changes

**Valid Examples:**
```
feature/ICOE-34897-add-default-image
feature/LOGIC-123-add-partner-workflow
bugfix/LA-12345-fix-null-pointer
hotfix/ICOE-99999-patch-security
refactor/TECH-456-optimize-queries
```

**Invalid Examples:**
```
my-feature                      # No type or ticket
feature-ICOE-12345             # Wrong separator (use /)
feature/add-feature            # No ticket ID
Feature/ICOE-123-Test          # Type should be lowercase
feature/ICOE-123_test          # Use hyphens, not underscores
```

### Logic App Workflow Validation

When you commit `workflow.json` files, the hooks validate:

**Structure Checks:**
- Valid JSON syntax
- Required properties: `definition`, `kind`
- Required definition properties: `$schema`, `triggers`, `actions`
- Workflow kind is `Stateful` or `Stateless`

**Security Warnings:**
- Detects potential hardcoded credentials
- Flags actions with `password`, `secret`, `apikey`, `token` in content
- Warns about missing connections configuration

**What Gets Checked:**
```json
{
  "definition": {
    "$schema": "...",        // Required
    "triggers": { ... },     // Required
    "actions": { ... }       // Optional but should exist
  },
  "kind": "Stateful"        // Required: Stateful or Stateless
}
```

---

## Troubleshooting

### "Python not found"

**Problem:** Python 3 is not installed or not in PATH

**Solution:**
1. Install Python 3.8+ from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart terminal/command prompt
4. Verify: `python3 --version` (Mac/Linux) or `python --version` (Windows)
5. Rerun setup script

**Windows specific:**
```powershell
# Check if Python is in PATH
python --version

# If not found, add to PATH:
# System Properties → Environment Variables → Path → Edit
# Add: C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python3X
```

### "pre-commit: command not found"

**Problem:** pre-commit framework is not installed or not in PATH

**Solution:**
```bash
# Install manually
pip3 install --user pre-commit

# Mac/Linux - Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc

# Windows - pre-commit should be in:
# %USERPROFILE%\AppData\Local\Programs\Python\Python3X\Scripts

# Verify installation
pre-commit --version

# Rerun setup script
.dev-tools/setup/setup-hooks.sh  # or .bat
```

### "func: command not found"

**Problem:** Azure Functions Core Tools not installed

**Solution:**
```bash
# Windows
npm install -g azure-functions-core-tools@3 --unsafe-perm true

# Mac
brew tap azure/functions
brew install azure-functions-core-tools@3

# Linux
npm install -g azure-functions-core-tools@3 --unsafe-perm true

# Verify
func --version
```

### Hooks not running

**Problem:** Hooks are installed but not executing

**Solution:**
```bash
# Check if hooks are installed
ls -la .git/hooks/  # Mac/Linux
dir .git\hooks\     # Windows

# Should see: commit-msg, pre-commit, pre-push

# Reinstall hooks
pre-commit uninstall
pre-commit install --install-hooks
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

# Or rerun setup script
.dev-tools/setup/setup-hooks.sh  # or .bat
```

### "Permission denied" (Mac/Linux)

**Problem:** Scripts don't have execute permissions

**Solution:**
```bash
# Make setup scripts executable
chmod +x .dev-tools/setup/setup-hooks.sh
chmod +x .dev-tools/setup/setup-logic-apps.sh

# Make hook scripts executable
chmod +x .dev-tools/hooks/*.py

# Rerun setup
.dev-tools/setup/setup-hooks.sh
```

### "Azurite: Start" not working

**Problem:** Azurite is not installed or not starting

**Solution:**
```bash
# Install Azurite globally
npm install -g azurite

# Start Azurite manually
azurite --silent --location ./azurite --debug ./azurite/debug.log

# Or in VS Code
# Press F1 → "Azurite: Start"

# Verify it's running
# Should see processes on ports 10000, 10001, 10002
```

### "Designer fails to open" in VS Code

**Problem:** Logic App designer won't open in VS Code

**Solution:**
1. Check Azurite is running: `F1` → `Azurite: Start`
2. Verify `local.settings.json` exists with:
```json
   {
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true"
     }
   }
```
3. Restart VS Code
4. Ensure Azure Logic Apps (Standard) extension is installed
5. Right-click `workflow.json` → "Open in Designer"

### Hooks triggering on wrong branch

**Problem:** Hooks are running on release/main branch

**Solution:**
This shouldn't happen, but if it does:

1. Check your current branch: `git branch`
2. Verify `common.py` has correct protected branches:
```python
   SKIP_BRANCHES = ['release', 'main', 'master']
```
3. If you use different branch names, update `SKIP_BRANCHES` in `.dev-tools/hooks/common.py`
4. Reinstall hooks: rerun setup script

### "Invalid JSON" error on workflow.json

**Problem:** JSON syntax error in workflow file

**Solution:**
```bash
# Validate JSON manually
# Mac/Linux
python3 -m json.tool workflow.json

# Or use online validator
# Copy content to: https://jsonlint.com/

# Common issues:
# - Missing commas
# - Trailing commas
# - Unquoted property names
# - Single quotes instead of double quotes
```

### Bypassing hooks (Emergency Only)

**Problem:** Need to commit urgently, hooks are blocking

**Solution:**
```bash
# Skip all hooks for one commit
git commit --no-verify -m "HOTFIX-123 | emergency fix"

# Skip pre-push hook
git push --no-verify

# WARNING: CI/CD pipeline will still validate!
# Fix the issues after your emergency commit
```

---

## File Structure
```
.dev-tools/
├── hooks/                          # Validation scripts
│   ├── common.py                   # Shared utilities
│   ├── validate_commit_msg.py      # Commit message validator
│   ├── validate_branch_name.py     # Branch name validator
│   └── validate_logic_app.py       # Logic App JSON validator
├── setup/                          # Setup scripts
│   ├── setup-hooks.sh              # Mac/Linux hook installer
│   ├── setup-hooks.ps1             # Windows hook installer
│   ├── setup-hooks.bat             # Windows hook wrapper
│   ├── setup-logic-apps.sh         # Mac/Linux Logic Apps tools
│   └── setup-logic-apps.ps1        # Windows Logic Apps tools
├── config/                         # Configuration
│   └── pre-commit-config.yaml      # Pre-commit framework config
└── README.md                       # This file
```

---

## Updating Hooks

When DevOps updates the hooks:
```bash
# Pull latest changes
git checkout dev
git pull origin dev

# Reinstall hooks to get updates
.dev-tools/setup/setup-hooks.sh  # or .bat

# Verify new version works
git commit --allow-empty -m "TEST-123 | test after update"
```

---

## For DevOps: Making Changes

To update hooks across all repositories:

1. Make changes in `.dev-tools/`
2. Test thoroughly in a test repository
3. Commit to dev branch:
```bash
   git add -f .dev-tools/
   git commit -m "TECH-001 | update git hooks validation"
   git push origin dev
```
4. Notify team to rerun setup scripts
5. Update documentation if behavior changes

---

## FAQ

### Q: Do I need to run setup for each repository?
**A:** Yes, git hooks are local to each repository. Run setup once per repo after cloning.

### Q: Can I customize the validation rules?
**A:** No, these are managed by DevOps. If you need changes, contact the DevOps team.

### Q: What if I don't have a ticket ID?
**A:** All code changes should have a ticket. For minor fixes without tickets, use:
- `TECH-XXX` for technical debt
- `CHORE-XXX` for maintenance tasks
- Ask your team lead to create a ticket

### Q: Do hooks run on merge commits?
**A:** Merge commits are automatically skipped. Hooks only validate your direct commits.

### Q: Will hooks slow down my workflow?
**A:** No, validation takes < 1 second. It's much faster than waiting for CI/CD to fail!

### Q: Can I use the designer without installing tools?
**A:** No, you need Azure Functions Core Tools and Azurite to use the Logic App designer locally in VS Code.

### Q: What happens if I bypass hooks?
**A:** Local hooks can be bypassed with `--no-verify`, but the CI/CD pipeline will still validate your code and may block your PR.

---

## Support

- **Setup Issues:** Rerun setup scripts or see troubleshooting above
- **Hook Behavior Questions:** Contact DevOps team
- **Bug Reports:** Create a ticket or message DevOps
- **Feature Requests:** Discuss with team lead

---

## Version History

- **v1.0** - Initial release with commit/branch validation
- **v1.1** - Added Logic App workflow validation
- **v1.2** - Added Logic Apps local development tools setup

---

**Questions?** Don't hesitate to reach out!

**Remember:** These tools are here to help you catch issues early and maintain code quality.

**Happy Coding!!**