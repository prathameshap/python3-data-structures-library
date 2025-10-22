# [Your Repo Name]

[Brief description of what this project does]

Example:
> Event-driven microservice for loyalty partner integrations. Processes account events via Kafka and orchestrates workflows with external partner APIs using Azure Logic Apps and Functions.

---

## Quick Start for New Developers

### Prerequisites

**Common (All Projects):**
- Git
- Python 3.8+ (for dev tools)
- Visual Studio Code
- Azure CLI (optional, for deployment) //We use Jenkins pipeline for deployment

**For Logic Apps Projects:**
- Node.js 14+ LTS //Or current repo recommended version
- .NET Core 3.1+ SDK //Or current repo recommended version
- Azure Functions Core Tools v3
- Azurite (local storage emulator)

**For Java Function Apps:**
- Java 11+ (JDK)
- Maven 3.6+
- Azure Functions Core Tools v3 (optional) //to run local emulator

**For C# Function Apps:**
- .NET Core 3.1+ SDK or .NET 6+
- Azure Functions Core Tools v3
- Visual Studio 2019+ or VS Code

### 1. Clone Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. REQUIRED: Install Git Hooks (One Time Per Repo)

**Windows:**
```cmd
.dev-tools\setup\setup-hooks.bat
```

**Mac/Linux:**
```bash
chmod +x .dev-tools/setup/setup-hooks.sh
.dev-tools/setup/setup-hooks.sh
```

**Takes ~1 minute. Must be done for each repository you work on.**

This installs Git hooks that enforce:
- Commit message format
- Branch naming conventions
- Code quality checks

### 3. Project-Specific Setup

#### For Logic Apps Projects:

**Install Development Tools:**

**Windows:**
```powershell
.\.dev-tools\setup\setup-logic-apps.ps1
```

**Mac/Linux:**
```bash
chmod +x .dev-tools/setup/setup-logic-apps.sh
.dev-tools/setup/setup-logic-apps.sh
```

**Install VS Code Extensions:**
- Azure Logic Apps (Standard)
- Azure Functions
- Azure Account
- Azurite

**Create local settings:**
```bash
# Copy template
cp local.settings.json.example local.settings.json

# Edit with your configuration
# Add connection strings, API keys, etc.
```

**Start local development:**
```bash
# Start Azurite (in VS Code: F1 → "Azurite: Start")
# Or from command line:
azurite --silent --location ./azurite

# Start Logic App
func start
```

#### For Java Function Apps:

**Build the project:**
```bash
mvn clean install
```

**Run tests:**
```bash
mvn test
```

**Run locally:**
```bash
mvn azure-functions:run
# Or
mvn spring-boot:run
```

**Create local settings:**
```bash
# Copy template if exists
cp local.settings.json.example local.settings.json

# Or create application.properties
cp application.properties.example application.properties
```

#### For C# Function Apps:

**Restore dependencies:**
```bash
dotnet restore
```

**Build:**
```bash
dotnet build
```

**Run locally:**
```bash
func start
# Or
dotnet run
```

### 4. Verify Setup Works
```bash
# Test commit message validation
git commit --allow-empty -m "bad message"
# Expected: ERROR

# Test with correct format
git commit --allow-empty -m "TEST-123 | test commit message"
# Expected: Success

# Clean up test commit
git reset --soft HEAD~1
```

If validation works, you're ready to develop!

---

## Development Workflow

### Standard Workflow (Dev Branch)
```bash
# 1. Start from Dev branch
git checkout dev
git pull origin dev

# 2. Create your feature branch (hooks validate name)
git checkout -b feature/TICKET-123-add-new-feature

# 3. Make changes
# - Logic Apps: Edit workflows in VS Code designer or JSON
# - Java: Edit .java files
# - C#: Edit .cs files

# 4. Test locally
# Logic Apps: func start
# Java: mvn test
# C#: dotnet test

# 5. Commit with proper format (hooks validate message)
git add .
git commit -m "TICKET-123 | implement new feature logic"

# 6. Push to remote (hooks validate branch name)
git push origin feature/TICKET-123-add-new-feature

# 7. Create Pull Request to Dev branch in Azure DevOps
```

**DO NOT DIRECTLY COMMIT TO 'DEV' BRANCH**

### Commit Message Format

**Required Format:** `TICKET-ID | description`

**Good Examples:**
```
ICOE-34897 | add null check for altImage with fallback
LA-12345 | fix authentication timeout issue
LOGIC-456 | add new workflow for partner sync
FUNC-789 | refactor error handling in processor
TECH-001 | update dependencies to latest versions
```

**Bad Examples:**
```
fixed bug          (no ticket ID)
ICOE-34897 fixed   (missing pipe |)
added feature      (past tense, no ticket)
update code        (no ticket ID)
```

**Rules:**
- Must start with uppercase ticket ID (e.g., ICOE-123, LA-456, LOGIC-789)
- Must have space, pipe `|`, space after ticket ID
- Description should use imperative mood (add, fix, update, refactor)
- NOT past tense (added, fixed, updated)
- Keep first line under 100 characters
- Can add details on additional lines

### Branch Naming Convention

**Required Format:** `type/TICKET-ID-short-description`

**Valid Types:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `refactor/` - Code refactoring
- `test/` - Test additions/updates
- `docs/` - Documentation changes

**Good Examples:**
```
feature/ICOE-34897-add-default-image
feature/LOGIC-123-add-partner-workflow
feature/FUNC-456-add-kafka-consumer
bugfix/LA-12345-fix-null-pointer
hotfix/ICOE-99999-patch-security-vulnerability
refactor/TECH-789-optimize-database-queries
```

**Bad Examples:**
```
my-feature                      (no type or ticket)
feature-ICOE-12345             (wrong separator, use /)
feature/add-feature            (no ticket ID)
Feature/ICOE-123-Test          (type should be lowercase)
feature/ICOE-123_test          (use hyphens, not underscores)
```

---

## Project Structure

### Logic Apps Project Structure:
https://docs.microsoft.com/en-us/azure/logic-apps/create-single-tenant-workflows-visual-studio-code#project-structure
```
your-logic-app-repo/
├── .dev-tools/              # Dev tools & git hooks (don't modify!)
├── workflows/               # Logic App workflows
│   ├── AccountLinking/
│   │   ├── workflow.json   # Workflow definition
│   │   └── function.json   # Trigger binding
│   ├── AccountUnlinking/
│   └── PartnerSync/
├── lib/                     # Custom code/assemblies
├── Artifacts/              # Maps, schemas, connectors
│   ├── Maps/
│   ├── Schemas/
│   └── Connectors/
├── .vscode/                # VS Code configuration
│   ├── extensions.json
│   ├── settings.json
│   └── launch.json
├── connections.json        # API connections
├── host.json              # Function host settings
├── local.settings.json.example
├── parameters.json        # Workflow parameters
└── README.md             # This file
```

### Java Function App Structure:
https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-java
```
your-java-function-repo/
├── .dev-tools/              # Dev tools & git hooks (don't modify!)
├── src/
│   ├── main/
│   │   ├── java/           # Java source code
│   │   │   └── com/company/
│   │   │       ├── functions/     # Azure Functions
│   │   │       ├── services/      # Business logic
│   │   │       ├── models/        # DTOs
│   │   │       └── utils/         # Utilities
│   │   └── resources/      # Configuration files
│   │       ├── application.properties
│   │       └── logback.xml
│   └── test/              # Unit & integration tests
│       └── java/
├── pom.xml                # Maven configuration
├── local.settings.json.example
└── README.md
```

### C# Function App Structure:
https://docs.microsoft.com/en-us/azure/azure-functions/functions-dotnet-class-library
```
your-csharp-function-repo/
├── .dev-tools/              # Dev tools & git hooks (don't modify!)
├── Functions/              # Azure Functions
│   ├── HttpTrigger.cs
│   └── TimerTrigger.cs
├── Services/              # Business logic
├── Models/               # DTOs
├── Utils/                # Utilities
├── host.json
├── local.settings.json.example
├── YourProject.csproj
└── README.md
```
##NOTE: Please adhere to standard structures of each
---

## Documentation

- **[ONBOARDING.md](ONBOARDING.md)** - Complete setup guide for new developers
- **[Git Processes.docx](Git%20Processes.docx)** - Git standards & conventions
- **[Code Standards.docx](Code%20Standards.docx)** - Coding standards (Java/C#)
- **[.dev-tools/README.md](.dev-tools/README.md)** - Git hooks troubleshooting

---

## Technology Stack

## Code Quality Standards

This project uses automated code quality checks to maintain consistency and best practices.

### Checkstyle Integration

**For Java Projects:**
- Runs automatically on every commit
- Validates code against team standards
- **Style violations show as warnings** (don't block commits)
- **Only critical errors block commits** (syntax, compilation issues)
- Provides immediate feedback

**Quick Check:**
```bash
# Run Checkstyle before committing
mvn checkstyle:check

# Generate detailed report
mvn checkstyle:checkstyle
# View: target/site/checkstyle.html
```

**Warnings (Don't Block Commits):**
- Missing JavaDoc on public methods
- Incorrect naming conventions
- Method too long (>150 lines)
- Style violations

**Errors (Block Commits):**
- Star imports (import java.util.*)
- Syntax errors
- Compilation issues

**See:** [Code Standards.docx](Code%20Standards.docx) for detailed standards

**Configuration:** `checkstyle.xml` in repository root

**Skip (Emergency):** `mvn clean package -DskipCheckstyle=true`

**Common:**
- **Cloud:** Azure (Logic Apps, Functions, Key Vault, Service Bus, Storage)
- **Source Control:** Git, Azure DevOps
- **CI/CD:** Azure DevOps Pipelines

**Logic Apps Specific:**
- **Runtime:** Azure Logic Apps (Standard)
- **Workflow Engine:** Azure Functions Runtime
- **Local Development:** VS Code + Azure Logic Apps extension
- **Storage Emulation:** Azurite

**Java Function Apps Specific:**
- **Language:** Java 11
- **Framework:** Spring Boot / Azure Functions Java
- **Build Tool:** Maven
- **Testing:** JUnit, Mockito

**C# Function Apps Specific:**
- **Language:** C# (.NET Core 3.1 or .NET 6+)
- **Framework:** Azure Functions .NET
- **Build Tool:** dotnet CLI
- **Testing:** xUnit, Moq

**Common Integrations:**
- **Messaging:** Apache Kafka, Azure Service Bus
- **Authentication:** OAuth2, Azure AD
- **Monitoring:** Application Insights, Azure Monitor

---

## Configuration

### Environment Variables

**Common:**
```bash
# Azure Configuration
AZURE_KEYVAULT_URL=https://your-vault.vault.azure.net/
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Application Insights
APPINSIGHTS_INSTRUMENTATIONKEY=your-instrumentation-key
```

**Logic Apps Specific:**
```bash
# Required for local development
AzureWebJobsStorage=UseDevelopmentStorage=true
FUNCTIONS_WORKER_RUNTIME=node
APP_KIND=workflowApp

# API Connections
PARTNER_API_URL=https://api.partner.com
OAUTH_TOKEN_URL=https://auth.partner.com/token //Not applicabel for most of our repos
```

**Java/C# Function Apps Specific:**
```bash
# Kafka Configuration
KAFKA_BROKERS=your-kafka-brokers
KAFKA_TOPIC=your-topic
KAFKA_CONSUMER_GROUP=your-consumer-group

# Database (if applicable)
DATABASE_CONNECTION_STRING=your-connection-string

# API Configuration
API_BASE_URL=https://api.example.com
API_KEY=your-api-key //This is name of the varibale referencing the API key
```

### Local Development Setup

#### Logic Apps:
1. Copy `local.settings.json.example` to `local.settings.json`
2. Fill in your configuration values
3. Start Azurite: `F1` → `Azurite: Start` (in VS Code)
4. Run: `func start`
5. Access: `http://localhost:7071`

#### Java Function Apps:
1. Copy `application.properties.example` to `application.properties`
2. Fill in your configuration values
3. Build: `mvn clean install`
4. Run: `mvn azure-functions:run` or `mvn spring-boot:run`
5. Access: `http://localhost:7071` (Functions) or `http://localhost:8080` (Spring Boot)

#### C# Function Apps:
1. Copy `local.settings.json.example` to `local.settings.json`
2. Fill in your configuration values
3. Build: `dotnet build`
4. Run: `func start` or `dotnet run`
5. Access: `http://localhost:7071`

**Note:** `local.settings.json` and `application.properties` are in `.gitignore` and should NEVER be committed!

---

## Testing

### Logic Apps:
```bash
# Start locally
func start

# Test workflow trigger (HTTP trigger example)
curl -X POST http://localhost:7071/runtime/webhooks/workflow/api/management/workflows/YourWorkflow/triggers/manual/run?api-version=2020-05-01-preview

# View run history in VS Code
# Azure Logic Apps extension → Show Run History

# Test in Azure Portal after deployment
```

### Java Function Apps:
```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=YourTestClass

# Run integration tests
mvn verify -P integration-tests

# Generate test coverage report
mvn clean test jacoco:report
# View: target/site/jacoco/index.html

# Run single test method
mvn test -Dtest=YourTestClass#testMethod
```

### C# Function Apps:
```bash
# Run all tests
dotnet test

# Run specific test project
dotnet test YourProject.Tests/

# Run tests with coverage
dotnet test /p:CollectCoverage=true

# Run specific test
dotnet test --filter "FullyQualifiedName~YourNamespace.YourTestClass.YourTestMethod"
```

---

## Deployment

### Dev Environment
```bash
# Automatic deployment on merge to dev branch
# Via Azure DevOps pipeline
# Triggered by: PR merge to dev
```

### QA Environment
```bash
# Deployment when dev is merged to release
# Requires: QA team approval
# Triggered by: PR from dev to release
```

### Production
```bash
# Manual deployment from release branch
# Requires: Tech lead + product owner approval
# Triggered by: Manual pipeline run
```

### Manual Deployment (if needed)

#### Logic Apps (via VS Code):
```
1. Right-click on workflow folder
2. Select "Deploy to Logic App..."
3. Choose subscription
4. Select target Logic App
5. Confirm deployment
```

#### Via Azure CLI:
```bash
# Logic Apps
az logicapp deployment source config-zip \
  --resource-group <resource-group> \
  --name <logic-app-name> \
  --src <zip-file>

# Function Apps (Java/C#)
func azure functionapp publish <function-app-name>

# Or using Maven (Java)
mvn azure-functions:deploy
```

---

## Important Notes

### Git Hooks Behavior

| Branch Type | Hooks Active? | Why?                                 |
|-------------|---------------|--------------------------------------|
| dev         |  Yes          | Enforce standards during development |
| feature/*   |  Yes          | Validate all feature work            |
| bugfix/*    |  Yes          | Validate all bug fixes               |
| hotfix/*    |  Yes          | Validate critical fixes              |
| refactor/*  |  Yes          | Validate refactoring                 |
| test/*      |  Yes          | Validate test changes                |
| docs/*      |  Yes          | Validate documentation               |
| **release** |  No           | Don't block release merges           |
| **master**  |  No           | Don't block production deploys       |

**Why skip on release/main/master?**
- These are protected branches for production deployment
- Code already validated on feature/dev branches
- Avoids blocking critical releases

### CI/CD Validation

All PRs are automatically validated for:
- Commit message format
- Branch naming convention
- Code quality (Checkstyle for Java, basic checks for C#)
- Workflow validation (Logic Apps)
- Build succeeds
- Tests pass

**Code Quality Behavior:**
- **Style violations** (naming, JavaDoc, method length) show as warnings with file:line:column information
- **Critical errors** (syntax, compilation, star imports) block commits with precise file:line:column location
- **Commit messages and branch naming** still enforced strictly

### Enhanced Error Reporting

All validation tools now provide detailed file location information:

- **Java Checkstyle**: `src/main/java/Example.java:23:5: Missing JavaDoc comment`
- **C# Analysis**: `Program.cs:15:8: CS0168 - Variable 'x' is declared but never used`
- **Logic Apps**: `workflow.json:12: Invalid JSON - Expecting ',' delimiter`

This format enables:
- **Quick Navigation**: Click errors to jump directly to file locations
- **IDE Integration**: Compatible with most editors and IDEs
- **Precise Debugging**: Exact line and column numbers for targeted fixes

Even if you bypass local hooks (`--no-verify`), the Azure DevOps pipeline will still validate!

**Bypassing hooks may cause pipeline failures!**

---

## Troubleshooting

### Common Issues

#### "Hooks not running"
- Did you run the setup script? See Quick Start section
- Rerun: `.dev-tools/setup/setup-hooks.sh` (or `.bat`)

#### "Python not found"
- Install Python 3.8+ from https://python.org
- Check "Add Python to PATH" during installation
- Restart terminal and rerun setup

#### "Permission denied" (Mac/Linux)
```bash
chmod +x .dev-tools/setup/setup-hooks.sh
.dev-tools/setup/setup-hooks.sh
```

### Logic Apps Specific

#### "Designer fails to open"
1. Check Azurite is running: `F1` → `Azurite: Start`
2. Verify `local.settings.json` exists with `AzureWebJobsStorage=UseDevelopmentStorage=true`
3. Restart VS Code
4. Ensure Azure Logic Apps (Standard) extension installed

#### "func: command not found"
```bash
npm install -g azure-functions-core-tools@3 --unsafe-perm true
```

#### "Workflow won't trigger"
- Check `workflow.json` syntax
- Verify triggers are configured
- Check `local.settings.json` has all variables
- Review logs: `func start --verbose`

### Java Specific

#### "Build fails"
```bash
# Clean and rebuild
mvn clean install -U

# Skip tests temporarily
mvn clean install -DskipTests
```

#### "Tests fail"
```bash
# Run with detailed output
mvn test -X

# Check for compilation errors
mvn compile
```

### C# Specific

#### "Build fails"
```bash
# Clean and rebuild
dotnet clean
dotnet build

# Restore packages
dotnet restore
```

#### "Runtime error"
```bash
# Check .NET version
dotnet --version

# Ensure correct framework
dotnet --list-sdks
```

### More Help
- See [.dev-tools/README.md](.dev-tools/README.md) for detailed troubleshooting
- Contact DevOps team
- Check Azure DevOps wiki

---

## Contributing

### Development Standards

**All Projects:**
1. Run setup script (see Quick Start)
2. Create feature branch with proper naming
3. Write code following our standards
4. Write/update tests
5. Test locally before committing
6. Commit with proper message format
7. Push and create PR to `dev` branch
8. Address review feedback
9. Get approval and merge

**Logic Apps Specific:**
- Use workflow designer for visual editing
- Test locally with Azurite before committing
- Don't hardcode credentials in `workflow.json`
- Use parameters for environment-specific values
- Document complex workflows in comments

**Java Specific:**
- Add JavaDoc for all public classes and methods (shows as warning with file:line:column if missing)
- Follow naming conventions in Code Standards.docx (shows as warning with file:line:column if incorrect)
- Write unit tests for new features (min 80% coverage)
- Run Checkstyle before committing: `mvn checkstyle:check`
- **Style violations show as warnings** with precise file:line:column information and don't block commits
- **Only critical errors** (syntax, compilation, star imports) block commits with file:line:column location

**C# Specific:**
- Add XML documentation comments for public APIs (shows as warning with file:line:column if missing)
- Follow C# coding conventions (shows as warning with file:line:column if incorrect)
- Write unit tests for new features
- Run code analysis: `dotnet build /p:RunAnalyzers=true`
- **Style violations show as warnings** with precise file:line:column information and don't block commits
- **Only critical errors** (syntax, compilation) block commits with file:line:column location

**DO NOT DIRECTLY COMMIT TO 'DEV' BRANCH**

---

## Emergency Bypass

In rare emergencies, you can bypass hooks:
```bash
# Skip commit validation
git commit --no-verify -m "HOTFIX-123 | emergency production fix"

# Skip push validation
git push --no-verify
```

**Warning:** CI/CD pipeline will still validate! Bypassing hooks may cause pipeline failures.

**Use only for:**
- Critical production hotfixes
- Urgent security patches
- Build/deployment issues blocking release

**Do NOT use for:**
- "I forgot the format"
- "I don't have time"
- "Just want to commit quickly"

---

## Support

- **Setup Issues:** [.dev-tools/README.md](.dev-tools/README.md)
- **Git Standards:** [Git Processes.docx](Git%20Processes.docx)
- **Code Standards:** [Code Standards.docx](Code%20Standards.docx)
- **Team Chat:** [Your Teams/Slack Channel]
- **DevOps Team:** [Contact Email/Teams]
- **Documentation:** [Azure DevOps Wiki URL]
- **On-Call:** [PagerDuty/On-Call Schedule]

---

## Team

- **Tech Lead:** [Name]
- **Product Owner:** [Name]
- **DevOps Lead:** [Name]
- **Team Members:** [Names or link to team page]

---

## Related Repositories

- [Partner API Client Library](link)
- [Shared Models](link)
- [Common Utilities](link)
- [Integration Tests](link)

---

## Project Information

- **Project Started:** [Date]
- **Current Version:** [version]
- **Last Updated:** [Date]
- **Tech Stack Updated:** [Date]

---

## Recent Updates

### v2.1.0 (October 2025)
- Added automated git hooks for code quality
- Implemented Logic Apps workflow validation
- Updated to Java 11 / .NET 6
- Added comprehensive integration tests
- Improved error handling and logging

### v2.0.0 (September 2025)
- Complete refactoring of message processing
- Added retry mechanism with exponential backoff
- Implemented dead letter queue
- Enhanced monitoring and alerting

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

## Learning Resources

### New to the Project?
1. Read [ONBOARDING.md](ONBOARDING.md) //Update the link
2. Review [Git Processes.docx](Git%20Processes.docx) //Update the link
3. Study [Code Standards.docx](Code%20Standards.docx) //Update the link
4. Pair with team member on first ticket

### Technology Documentation

**Logic Apps:**
- [Azure Logic Apps Standard Docs](https://docs.microsoft.com/azure/logic-apps/single-tenant-overview-single-tenant)
- [Logic Apps Connectors](https://docs.microsoft.com/connectors/)
- [Workflow Definition Language](https://docs.microsoft.com/azure/logic-apps/logic-apps-workflow-definition-language)

**Azure Functions:**
- [Azure Functions Overview](https://docs.microsoft.com/azure/azure-functions/)
- [Azure Functions Java Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-java)
- [Azure Functions C# Guide](https://docs.microsoft.com/azure/azure-functions/functions-dotnet-class-library)

**Java Specific:**
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Maven Documentation](https://maven.apache.org/guides/)

**C# Specific:**
- [.NET Documentation](https://docs.microsoft.com/dotnet/)
- [C# Programming Guide](https://docs.microsoft.com/dotnet/csharp/)

**Azure Services:**
- [Azure Key Vault](https://docs.microsoft.com/azure/key-vault/)
- [Azure Service Bus](https://docs.microsoft.com/azure/service-bus-messaging/)
- [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)

---

## License

[Your License - e.g., Proprietary, MIT, Apache 2.0] //Not Applicable in our case

---

**Questions?** Don't hesitate to ask in the team chat or reach out directly!

**Happy coding!**
