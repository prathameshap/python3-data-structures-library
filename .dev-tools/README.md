# Development Tools Framework

**DO NOT MODIFY FILES IN THIS DIRECTORY** - Managed by DevOps

## Overview

This development framework provides automated validation for:
- Git commit message format
- Branch naming conventions  
- Code quality checks (Checkstyle for Java)
- Logic App workflow validation

## Quick Setup

### Prerequisites
- Git
- Python 3.8+
- For Java projects: Maven 3.6+
- For Logic Apps: Node.js 14+ LTS, .NET Core 3.1+ SDK

### Installation

**Windows:**
```cmd
.dev-tools\setup\setup-hooks.bat
```

**Mac/Linux:**
```bash
chmod +x .dev-tools/setup/setup-hooks.sh
.dev-tools/setup/setup-hooks.sh
```

**Optional - Logic Apps Tools:**
```bash
# Windows
.\.dev-tools\setup\setup-logic-apps.ps1

# Mac/Linux  
chmod +x .dev-tools/setup/setup-logic-apps.sh
.dev-tools/setup/setup-logic-apps.sh
```

### Verification
```bash
# Test commit message validation
git commit --allow-empty -m "TEST-123 | test message"
# Expected: SUCCESS: Commit message format is valid

# Test branch name validation
git checkout -b feature/TEST-123-test-branch
# Expected: SUCCESS: Branch name is valid
```

---

## Git Hooks Overview

### What Gets Installed
1. **commit-msg** - Validates commit message format
2. **pre-commit** - Validates Logic App JSON files and runs Checkstyle
3. **pre-push** - Validates branch naming convention

### Hooks Behavior

| Branch Type | Hooks Active? | Reason |
|-------------|---------------|--------|
| dev         | Yes           | Enforce standards during development |
| feature/*   | Yes           | Validate all feature work |
| bugfix/*    | Yes           | Validate all bug fixes |
| hotfix/*    | Yes           | Validate all hotfixes |
| refactor/*  | Yes           | Validate all refactoring |
| test/*      | Yes           | Validate all test changes |
| docs/*      | Yes           | Validate all documentation changes |
| **release** | No            | Don't block release merges |
| **main**    | No            | Don't block production deploys |
| **master**  | No            | Don't block production deploys |

**Why skip on release/main/master?**
- These are protected branches for production deployment
- Hooks running on feature/dev branches already validated the code
- Avoids blocking critical releases

---

## Validation Rules

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
ICOE-34897 fixed stuff     # Missing pipe |
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
- `bugfix/` - Bug fixes (for prod bugs since we do not create new branches for dev bugs)
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

## Code Quality Checks (Checkstyle)

### What is Checkstyle?

Checkstyle is a code quality tool that validates Java code against coding standards. It runs automatically during commits if you have Java files.

### When Does Checkstyle Run?

**Local Development:**
```bash
# Automatically runs when you commit Java files
git commit -m "ICOE-123 | add new service"
Running Java code quality checks...
Running Checkstyle...
Found 3 Checkstyle warning(s):
  src/main/java/com/example/Service.java:23:5: Missing JavaDoc comment
  src/main/java/com/example/Service.java:45:12: Method length is 160 lines (max 150)
  src/main/java/com/example/Service.java:67:8: Variable name 'user_id' should be camelCase
Warnings do not block commit. Run for details:
  mvn checkstyle:check
SUCCESS: Java code quality checks passed with warnings
```

**Manual Run:**
```bash
# Check your code manually before committing
mvn checkstyle:check

# Generate HTML report
mvn checkstyle:checkstyle
# View: target/site/checkstyle.html
```

### Checkstyle Behavior

**Warnings (Don't Block Commits):**
- Naming convention violations (shows as `filename:line:column: message`)
- JavaDoc missing (shows as `filename:line:column: Missing JavaDoc comment`)
- Method length violations (shows as `filename:line:column: Method length is 150 lines`)
- Style violations (shows as `filename:line:column: message`)
- Whitespace issues (shows as `filename:line:column: message`)

**Errors (Block Commits):**
- Syntax errors (shows as `filename:line:column: Syntax error message`)
- Compilation issues (shows as `filename:line:column: Compilation error`)
- Critical code quality issues (star imports, unused imports) (shows as `filename:line:column: message`)

**Commit/Push Failures:**
- Invalid commit message format
- Invalid branch naming convention

### Enhanced Error Reporting

All validation tools now provide detailed file location information in a consistent format:

**Java Checkstyle Output:**
```
src/main/java/com/example/Service.java:23:5: Missing JavaDoc comment
src/main/java/com/example/Service.java:45:12: Method length is 160 lines (max 150)
src/main/java/com/example/Service.java:67:8: Variable name 'user_id' should be camelCase
```

**C# Analysis Output:**
```
Program.cs:15:8: CS0168 - Variable 'x' is declared but never used
Program.cs:23:12: CS0219 - Variable 'y' is assigned but never used
Program.cs:45:5: CS1591 - Missing XML comment for publicly visible type
```

**Logic Apps Validation Output:**
```
workflow.json:12: Invalid JSON - Expecting ',' delimiter
workflow.json:45: Missing required property "triggers"
connections.json:8: May contain hardcoded credentials
```

**Benefits:**
- **Quick Navigation**: Click errors to jump directly to file locations in your IDE
- **IDE Integration**: Compatible with Visual Studio, VS Code, IntelliJ, and other editors
- **Precise Debugging**: Exact line and column numbers for targeted fixes
- **Consistent Format**: Uniform error reporting across all validation types

### What Does Checkstyle Validate?

**Naming Conventions (Warnings):**
- Class names (PascalCase)
- Method names (camelCase)
- Variable names (camelCase)
- Constants (UPPER_SNAKE_CASE)

**Code Structure (Warnings):**
- Method length (max 150 lines)
- Parameter count (max 7 parameters)
- Proper use of braces
- Import organization

**JavaDoc Requirements (Warnings):**
- Public classes must have JavaDoc
- Public methods must have JavaDoc
- Include @param, @return, @throws tags

**Code Style (Warnings):**
- Whitespace and indentation
- Proper modifier order

**Critical Issues (Errors - Block Commits):**
- No star imports (import java.util.*)
- Unused imports
- Syntax errors
- Compilation issues

### Maven Configuration

**Required `pom.xml` setup:**

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.0</version>
            <configuration>
                <configLocation>checkstyle.xml</configLocation>
                <encoding>UTF-8</encoding>
                <consoleOutput>true</consoleOutput>
                <failsOnError>true</failsOnError>
            </configuration>
            <executions>
                <execution>
                    <id>validate</id>
                    <phase>validate</phase>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**Plugin Configuration Explained:**
- `configLocation`: Points to your `checkstyle.xml` file
- `encoding`: File encoding for proper character handling
- `consoleOutput`: Shows violations in console
- `failsOnError`: Fails build on violations
- `executions`: Binds Checkstyle to Maven lifecycle

**Alternative: Checkstyle as Dependency**
```xml
<dependency>
    <groupId>com.puppycrawl.tools</groupId>
    <artifactId>checkstyle</artifactId>
    <version>10.12.0</version>
</dependency>
```

### Common Checkstyle Violations and Fixes

#### 1. Missing JavaDoc

**Violation:**
```java
public class AccountService {
    public void processAccount(String accountId) {
        // ...
    }
}
```

**Fixed:**
```java
/**
 * Service for processing customer accounts.
 */
public class AccountService {

    /**
     * Processes an account by its ID.
     *
     * @param accountId the account identifier
     * @throws IllegalArgumentException if accountId is null
     */
    public void processAccount(String accountId) {
        // ...
    }
}
```

#### 2. Incorrect Naming

**Violation:**
```java
public class accountService {  // Should be PascalCase
    private String Account_Id;  // Should be camelCase

    public void Process_Account() {  // Should be camelCase
    }
}
```

**Fixed:**
```java
public class AccountService {
    private String accountId;

    public void processAccount() {
    }
}
```

#### 3. Star Imports

**Violation:**
```java
import java.util.*;
import com.company.service.*;
```

**Fixed:**
```java
import java.util.List;
import java.util.ArrayList;
import com.company.service.AccountService;
import com.company.service.ValidationService;
```

#### 4. Method Too Long

**Violation:**
```java
public void processAccount() {
    // 200 lines of code
    // Checkstyle max is 150 lines
}
```

**Fixed:**
```java
public void processAccount() {
    validateAccount();
    enrichAccountData();
    saveAccount();
}

private void validateAccount() {
    // Validation logic
}

private void enrichAccountData() {
    // Enrichment logic
}

private void saveAccount() {
    // Save logic
}
```

### Skipping Checkstyle (Emergency Only)

**In local commits:**
```bash
# Skip all hooks including Checkstyle
git commit --no-verify -m "HOTFIX-123 | emergency fix"
```

**In Maven build:**
```bash
# Skip Checkstyle in build
mvn clean package -DskipCheckstyle=true
```

**Warning:** Use sparingly! CI/CD may still enforce quality checks.

### Configuring Checkstyle Rules

**Location:** `checkstyle.xml` in repository root

**File Structure:**
```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">

<module name="Checker">
    <property name="severity" value="error"/>
    <property name="fileExtensions" value="java"/>

    <module name="TreeWalker">
        <!-- Your rules go here -->
    </module>
</module>
```

**Common Rule Categories:**

**Naming Conventions:**
- `TypeName` - Class names (PascalCase)
- `MethodName` - Method names (camelCase)
- `VariableName` - Variable names (camelCase)
- `ConstantName` - Constants (UPPER_SNAKE_CASE)

**Code Structure:**
- `MethodLength` - Method length limits
- `ParameterNumber` - Parameter count limits
- `AvoidStarImport` - Prevents `import java.util.*`

**JavaDoc Requirements:**
- `JavadocMethod` - Requires JavaDoc on public methods
- `JavadocType` - Requires JavaDoc on public classes
- `JavadocVariable` - Requires JavaDoc on public variables

**Customization Examples:**

**Make rules more lenient:**
```xml
<module name="MethodLength">
    <property name="max" value="200"/>  <!-- Increase from 150 -->
</module>
```

**Disable specific checks:**
```xml
<module name="JavadocMethod">
    <!-- Disable JavaDoc requirement -->
</module>
```

**Add new rules:**
```xml
<module name="LineLength">
    <property name="max" value="120"/>
</module>
```

**Configure existing rules:**
```xml
<module name="JavadocMethod">
    <property name="scope" value="public"/>
    <property name="allowMissingParamTags" value="false"/>
    <property name="allowMissingReturnTag" value="false"/>
</module>
```

### IDE Integration

**IntelliJ IDEA:**
1. Install Checkstyle-IDEA plugin
2. Settings → Tools → Checkstyle
3. Add configuration file: `checkstyle.xml`
4. Enable "Scan Scope: All sources"

**Eclipse:**
1. Install Eclipse Checkstyle Plugin
2. Preferences → Checkstyle
3. New → External Configuration File → `checkstyle.xml`
4. Set as default configuration

**VS Code:**
1. Install "Checkstyle for Java" extension
2. Set `java.checkstyle.configuration` to `${workspaceFolder}/checkstyle.xml`

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

### "Build fails with Checkstyle violations"

**Problem:**
```
[ERROR] src/main/java/com/company/Service.java:23:
[ERROR] Missing JavaDoc comment.
[ERROR] BUILD FAILURE
```

**Solutions:**

1. **Fix the violations** (Recommended):
```bash
# See all violations
mvn checkstyle:check

# Fix them and commit
git commit -m "ICOE-123 | fix checkstyle violations"
```

2. **Make rules less strict:**
   - Edit `checkstyle.xml`
   - Increase limits or disable checks
   - Commit changes

3. **Skip temporarily:**
```bash
mvn clean package -DskipCheckstyle=true
```

### "Checkstyle takes too long"

**Problem:** Build is slow due to Checkstyle

**Solution:** Check only changed files in hooks:
```bash
# Git hooks already do this
# Only staged .java files are checked
```

### "Different results locally vs Jenkins"

**Problem:** Checkstyle passes locally but fails in Jenkins

**Cause:** Different Checkstyle versions

**Solution:** Version is locked in pom.xml:
```xml
<dependency>
    <groupId>com.puppycrawl.tools</groupId>
    <artifactId>checkstyle</artifactId>
    <version>10.12.0</version>
</dependency>
```

Both local and Jenkins use same version.

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
│   ├── validate_logic_app.py       # Logic App JSON validator
│   ├── validate_java_code.py       # Java Checkstyle validator
│   └── validate_csharp_code.py     # C# code validator
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

## Files Required for Checkstyle

**Repository root:**
```
your-repo/
├── pom.xml                    # Contains Checkstyle plugin
├── checkstyle.xml             # Checkstyle rules
└── .dev-tools/
    └── hooks/
        └── validate_java_code.py  # Calls Maven Checkstyle
```

**All files must be committed to repository.**

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

**Q: Do I need to install Checkstyle separately?**  
A: No, Maven downloads it automatically when you build.

**Q: Will Checkstyle slow down my commits?**  
A: Slightly (5-15 seconds), but most violations are now warnings that don't block commits.

**Q: Can I customize the rules?**  
A: Yes, edit `checkstyle.xml`. Discuss with team first.

**Q: What if I disagree with a rule?**  
A: Discuss with team lead. Rules can be changed if there's consensus.

**Q: Does Checkstyle check test files?**  
A: Yes, both `src/main/java` and `src/test/java`.

**Q: Can Checkstyle auto-fix violations?**  
A: No, but your IDE can help format code. Use IDE's "Reformat Code" feature.

**Q: Is Checkstyle included in production?**  
A: No, it only runs during build, not in the deployed JAR.

**Q: What if Jenkins build fails due to Checkstyle?**  
A: Most violations are now warnings. Only critical errors (syntax, compilation) will fail builds.

**Q: Do style violations block my commits?**  
A: No, style violations (naming, JavaDoc, method length) now show as warnings with file:line:column information and don't block commits.

**Q: What violations still block commits?**  
A: Only critical errors like syntax errors, compilation issues, and star imports block commits. All errors show precise file:line:column location for quick fixing.

**Q: How do I navigate to errors quickly?**  
A: The new file:line:column format is compatible with most IDEs. You can click on error messages in VS Code, IntelliJ, or Visual Studio to jump directly to the problematic code.

**Q: Do I need to run setup for each repository?**
A: Yes, git hooks are local to each repository. Run setup once per repo after cloning.

**Q: Can I customize the validation rules?**
A: No, these are managed by DevOps. If you need changes, contact the DevOps team.

**Q: What if I don't have a ticket ID?**
A: All code changes should have a ticket. For minor fixes without tickets, use:
- `TECH-XXX` for technical debt
- `CHORE-XXX` for maintenance tasks
- Ask your team lead to create a ticket

**Q: Do hooks run on merge commits?**
A: Merge commits are automatically skipped. Hooks only validate your direct commits.

**Q: Will hooks slow down my workflow?**
A: No, validation takes < 1 second. Style violations show as warnings and don't block commits, making development faster!

**Q: Can I use the designer without installing tools?**
A: No, you need Azure Functions Core Tools and Azurite to use the Logic App designer locally in VS Code.

**Q: What happens if I bypass hooks?**
A: Local hooks can be bypassed with `--no-verify`, but the CI/CD pipeline will still validate your code and may block your PR.

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
- **v1.3** - Added Checkstyle integration for Java projects
- **v1.4** - Added C# code validation

---

**Questions?** Don't hesitate to reach out!

**Remember:** These tools are here to help you catch issues early and maintain code quality.

**Happy Coding!!**
