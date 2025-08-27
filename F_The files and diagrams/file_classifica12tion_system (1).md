# File System Classification Framework

## Overview
This classification system organizes files based on **function**, **technology stack**, and **lifecycle stage** to enable efficient agentic AI file management.

## Primary Classification Hierarchy

### 1. **CODE_AND_DEVELOPMENT**
Files containing source code, scripts, and development resources.

#### 1.1 **source_code**
- **programming_languages/**
  - `mql4/` - Trading platform code (Expert Advisors, indicators, scripts)
  - `python/` - Python source files, modules, packages
  - `javascript/` - JS/TS files, Node.js applications
  - `java/` - Java source files and packages
  - `cpp/` - C/C++ source files
  - `other_languages/` - Go, Rust, Ruby, etc.

- **frameworks_and_platforms/**
  - `fastapi/` - FastAPI applications and services
  - `express/` - Express.js applications
  - `react/` - React components and applications
  - `docker/` - Containerization files
  - `web_technologies/` - HTML, CSS, frontend assets

#### 1.2 **development_tools**
- **build_and_deployment/**
  - Makefiles, build scripts, CI/CD configurations
  - Docker compose files, Kubernetes manifests
  - Deployment automation scripts

- **testing/**
  - Unit tests, integration tests, performance tests
  - Test data, fixtures, mocks
  - Testing configuration files

- **development_utilities/**
  - Code generators, linters, formatters
  - Development scripts and tools
  - IDE configurations

### 2. **SYSTEM_ARCHITECTURE**
Files defining system structure, APIs, and integration patterns.

#### 2.1 **architecture_documentation**
- **system_design/**
  - Architecture decision records (ADRs)
  - System diagrams and specifications
  - API documentation and schemas
  - Integration patterns and protocols

- **frameworks_and_patterns/**
  - MCP server documentation
  - Agent framework blueprints
  - Workflow definitions
  - Service orchestration patterns

#### 2.2 **apis_and_interfaces**
- **api_definitions/**
  - OpenAPI/Swagger specifications
  - GraphQL schemas
  - REST API documentation
  - Protocol definitions

- **integration_specifications/**
  - Third-party API integrations
  - Data exchange formats
  - Communication protocols

### 3. **CONFIGURATION_AND_DATA**
Configuration files, data schemas, and structured data.

#### 3.1 **configuration_files**
- **application_config/**
  - Environment configurations (.env, config.yaml)
  - Application settings and parameters
  - Feature flags and toggles

- **infrastructure_config/**
  - Server configurations
  - Database connection strings
  - Monitoring and logging configurations

#### 3.2 **data_and_schemas**
- **database_schemas/**
  - SQL schema definitions
  - Migration scripts
  - Database documentation

- **data_formats/**
  - JSON schemas
  - YAML data files
  - CSV data files
  - XML configurations

### 4. **DOMAIN_SPECIFIC_SYSTEMS**
Files organized by business domain or specialized system.

#### 4.1 **trading_systems**
- **mql4_trading/**
  - Expert Advisors (EAs)
  - Custom indicators
  - Trading scripts and libraries
  - Risk management modules

- **signal_processing/**
  - Signal generation algorithms
  - Market data processors
  - Trading strategy implementations

- **risk_management/**
  - Risk calculation modules
  - Compliance monitoring
  - Performance tracking

#### 4.2 **ai_automation**
- **agents_and_workflows/**
  - AI agent configurations
  - Workflow definitions
  - Prompt engineering templates
  - Model configuration files

- **machine_learning/**
  - ML model definitions
  - Training data and scripts
  - Model evaluation tools

#### 4.3 **constraint_systems**
- **code_generation/**
  - Constraint definitions
  - Code templates
  - Quality gates and validators
  - Pattern libraries

### 5. **DOCUMENTATION_AND_STANDARDS**
Documentation, standards, and knowledge management files.

#### 5.1 **technical_documentation**
- **user_guides/**
  - Installation guides
  - User manuals
  - Tutorials and examples

- **developer_documentation/**
  - Technical specifications
  - Code style guides
  - Best practices documentation

#### 5.2 **standards_and_policies**
- **coding_standards/**
  - Language-specific style guides
  - Security guidelines
  - Performance standards

- **compliance_and_security/**
  - Security policies
  - Compliance frameworks
  - Audit documentation

### 6. **PROJECT_MANAGEMENT**
Project organization, planning, and management files.

#### 6.1 **project_structure**
- **project_definitions/**
  - Project overviews and blueprints
  - Scope and requirements documents
  - Project configuration files

- **organizational_structure/**
  - Team structures
  - Role definitions
  - Responsibility matrices

#### 6.2 **planning_and_tracking**
- **project_plans/**
  - Timeline and milestones
  - Resource allocation
  - Progress tracking

## File Type Extensions Mapping

### Programming Languages
```yaml
mql4: [.mq4, .mq5, .mqh]
python: [.py, .pyx, .pyi, .ipynb]
javascript: [.js, .jsx, .ts, .tsx, .mjs]
java: [.java, .class, .jar]
cpp: [.cpp, .c, .h, .hpp, .cc]
web: [.html, .css, .scss, .sass, .less]
```

### Configuration & Data
```yaml
config: [.yaml, .yml, .json, .toml, .ini, .conf, .config]
data: [.csv, .xml, .sql, .db, .sqlite]
environment: [.env, .env.local, .env.production]
```

### Documentation
```yaml
documentation: [.md, .rst, .txt, .pdf, .docx]
diagrams: [.png, .jpg, .svg, .drawio, .puml]
```

### Build & Deployment
```yaml
build: [Dockerfile, docker-compose.yml, Makefile, .gitignore]
ci_cd: [.github/, .gitlab-ci.yml, .jenkins, .travis.yml]
```

## Classification Rules for Agentic AI

### Primary Classification Algorithm
```python
def classify_file(file_path, content_analysis):
    # 1. Check file extension first
    extension_category = get_category_by_extension(file_path)
    
    # 2. Analyze directory structure context
    directory_context = analyze_directory_pattern(file_path)
    
    # 3. Content-based classification (for unclear cases)
    if extension_category is None:
        content_category = analyze_file_content(content_analysis)
        
    # 4. Apply domain-specific rules
    domain_category = apply_domain_rules(file_path, content_analysis)
    
    return merge_classifications(extension_category, directory_context, 
                               content_category, domain_category)
```

### Priority Rules
1. **Security-sensitive files** → Always classify as high-priority
2. **Active development** → Classify by current project phase
3. **Legacy/archive** → Separate archival classification
4. **Generated files** → Lower priority, potential cleanup candidates
5. **Configuration files** → High priority, careful handling required

### Cleanup Recommendations

#### Safe to Archive/Remove
- Duplicate files (based on content hash)
- Old build artifacts and compiled files
- Temporary files and caches
- Outdated documentation versions
- Unused dependency files

#### High Priority (Never Auto-Delete)
- Source code files
- Configuration files
- Documentation with no duplicates
- Database schemas and migrations
- Security-related files

#### Requires Human Review
- Files with mixed content types
- Files in ambiguous directory structures
- Files with custom extensions
- Files larger than typical for their type
- Files modified recently but in archived projects

## Implementation Guidelines

### For Agentic AI Systems
1. **Start with extension-based classification** (90% accuracy)
2. **Use directory structure context** for disambiguation
3. **Apply content analysis** only for unclear cases
4. **Maintain classification confidence scores**
5. **Flag uncertain classifications** for human review
6. **Use domain-specific rules** for specialized file types
7. **Track classification decisions** for learning/improvement

### Quality Assurance
- Validate classifications against known project structures
- Cross-reference with version control history
- Check for circular dependencies in classifications
- Ensure important files are never auto-deleted
- Maintain audit trail of all classification decisions