# Agent Project

> **A comprehensive AI agent operating system with hierarchical skill/prompt repositories, automatic quarantine systems, and a 5-layer configuration stack.**

---

## 🎯 What This Is

The Agent Project is a **complete AI agent infrastructure** that solves three hard problems:

1. **Identity & Values** — Who the agent is and what it won't do (SOUL)
2. **Knowledge Organization** — How to manage 1000+ skills without losing them (Skill Tree)
3. **Safety & Quality** — Automatic detection and quarantine of harmful content (Jail Systems)

Instead of scattered prompt files and flat skill directories, we use a **5-layer Agent OS** with Yahoo-style navigation, pointer-based single source of truth, and automatic decontamination pipelines.

---

## 🏛️ Agent OS — 5 Layer Stack

```mermaid
flowchart TB
    accTitle: Agent OS Configuration Stack
    accDescr: Five layers from identity at the top to role activation at the bottom, each constraining the layers below

    soul["🪨 Layer 1 — SOUL.md<br/>WHO the agent is<br/>Identity, values, ethics<br/>Loaded first, never changes"]
    
    agents["📋 Layer 2 — AGENTS.md<br/>HOW the agent works<br/>Behavioral rules, workflows<br/>Inheritable cascade"]
    
    tools["🔧 Layer 3 — TOOLS.md<br/>WHAT the agent can execute<br/>MCP servers, CLI, APIs<br/>Environment-specific"]
    
    skills["📚 Layer 4 — skills/<br/>WHAT the agent knows<br/>Hierarchical knowledge base<br/>On-demand loading"]
    
    prompts["🎭 Layer 5 — prompts/<br/>WHAT ROLE the agent plays<br/>Persona activation<br/>Optional context"]

    soul --> agents --> tools --> skills --> prompts

    classDef identity fill:#fce7f3,stroke:#db2777,stroke-width:3px,color:#831843
    classDef behavior fill:#dbeafe,stroke:#2563eb,stroke-width:3px,color:#1e3a5f
    classDef capability fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#14532d
    classDef knowledge fill:#fef9c3,stroke:#ca8a04,stroke-width:3px,color:#713f12
    classDef role fill:#ede9fe,stroke:#7c3aed,stroke-width:3px,color:#3b0764

    class soul identity
    class agents behavior
    class tools capability
    class skills knowledge
    class prompts role
```

### Layer 1: SOUL — Identity & Ethics

**File:** [`SOUL.md`](SOUL.md)

Defines who the agent is, what it values, and its ethical boundaries. This loads before everything else and **cannot be overridden**.

| Aspect | Description |
|--------|-------------|
| **Identity** | Technically precise, pragmatic senior engineer |
| **Core Values** | Precision over speed, honesty over comfort, evidence over assumption |
| **Ethical Boundaries** | Won't use stolen credentials, won't weaponize information, won't engage with CSAM |
| **Information Ethics** | Respects sensitivity lifecycle: active → decaying → public → eternal |

> **Key Principle:** Information moves through phases. Once it leaves the vault and enters the commons, we treat it as public record.

### Layer 2: AGENTS — Behavioral Rules

**File:** [`AGENTS.md`](AGENTS.md) (cascade through subdirectories)

Defines how the agent works — workflows, file organization, commit conventions, PR protocols.

```mermaid
flowchart TD
    accTitle: AGENTS.md Cascade Inheritance
    accDescr: Shows how AGENTS.md files cascade from root through domains to specific contexts

    root["📋 /AGENTS.md<br/>Repository root<br/>Base rules"]
    skills["📋 skills/AGENTS.md<br/>Skill tree<br/>Loading protocol"]
    domain["📋 skills/domain/AGENTS.md<br/>Domain-specific<br/>Workflow rules"]
    context["📋 Context AGENTS.md<br/>Task-specific<br/>Extensions"]

    root --> skills --> domain --> context

    classDef base fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
    classDef extend fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef specific fill:#fef3c7,stroke:#d97706,color:#92400e

    class root base
    class skills,domain extend
    class context specific
```

**Inheritance Rule:** Lower layers can extend but never contradict upper layers.

### Layer 3: TOOLS — Capabilities

**File:** [`TOOLS.md`](TOOLS.md)

What the agent can execute — MCP servers, CLI tools, APIs, environment capabilities.

| Category | Examples |
|----------|----------|
| **Browser** | Playwright for web automation, screenshots, testing |
| **Code** | LSP for navigation, AST-grep for refactoring, diagnostics |
| **Search** | Web search (Exa), GitHub search, Context7 for docs |
| **AI** | Oracle for architecture, Librarian for research, Subagents for delegation |

Tools are **declarative** — the agent reads TOOLS.md to understand what's available, then uses them as needed.

### Layer 4: SKILLS — Knowledge

**Directory:** [`skills/`](skills/)

The skill tree — hierarchical knowledge organized by domain. Skills are **on-demand** — loaded only when needed.

```mermaid
flowchart LR
    accTitle: Skill Tree Navigation
    accDescr: Three ways to find skills: drill-down navigation, grep index, or follow pointers

    User([User/Agent])
    
    subgraph "Navigation Layer"
        Domain["skills/domain/<domain>/"]
        Subdomain[".../<subdomain>/"]
        Pointer["<skill>.pointer.md"]
    end
    
    subgraph "Storage Layer"
        Canonical["skills/canonical/<source>/<skill>/SKILL.md"]
        Index["skills/INDEX.json<br/>(grep target)"]
    end

    User -->|Drill down| Domain
    Domain --> Subdomain --> Pointer
    User -->|Grep| Index
    Pointer -->|"follow canonical path"| Canonical

    classDef nav fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef store fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef user fill:#f3f4f6,stroke:#6b7280,color:#374151

    class Domain,Subdomain,Pointer,Index nav
    class Canonical store
    class User user
```

**Key Features:**
- **Yahoo Directory:** Drill down `domain/science/writing/`
- **Grep Index:** `jq '.[] | select(.tags[] | contains("python"))' skills/INDEX.json`
- **Pointer SSoT:** Every skill has one canonical path, no duplicates

See [`SKILL-TREE.md`](SKILL-TREE.md) for complete design.

### Layer 5: PROMPTS — Role Activation

**Directory:** [`prompts/`](prompts/)

Persona activation templates. When you need the agent to adopt a specific role (expert debugger, security auditor, etc.), you load a prompt from here.

**Structure mirrors skills exactly:**
- `prompts/domain/development/debugging/expert-debugger.pointer.md`
- Points to `prompts/canonical/imported/prompts-chat/expert-debugger/PROMPT.md`

See [`PROMPT-TREE.md`](PROMPT-TREE.md) for complete design.

---

## 🛡️ Jail Systems — Automatic Quarantine

```mermaid
flowchart TD
    accTitle: Jail System Workflow
    accDescr: Automatic quarantine, decontamination, and approval workflow for skills and prompts

    Import([Import/Detection])
    Scan{Auto-Scan}
    Clean[Direct Promote]
    Violation[Move to review-pending]
    Review{Manual Review}
    Approve[Approve]
    Quarantine[Move to quarantined]
    Block[Move to blocked]
    AutoClean[Auto-Clean]
    Cleaned[Move to cleaned/]
    Verify{Manual Verify}
    Staged[Move to staged/]
    Promote[Promote to canonical/]

    Import --> Scan
    Scan -->|Clean| Clean
    Scan -->|Violation| Violation
    
    Clean --> Canonical[/skills/canonical/]
    Violation --> Review
    
    Review -->|Approve| Approve
    Review -->|Quarantine| Quarantine
    Review -->|Block| Block
    
    Approve --> Canonical
    Block --> BlockedBlocked[/skill-jail/blocked/]
    
    Quarantine --> AutoClean
    AutoClean --> Cleaned
    Cleaned --> Verify
    Verify --> Staged
    Staged --> Promote
    Promote --> Canonical

    classDef clean fill:#d1fae5,stroke:#059669,color:#065f46
    classDef quarantine fill:#fef3c7,stroke:#d97706,color:#92400e
    classDef block fill:#fee2e2,stroke:#dc2626,color:#991b1b
    classDef process fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef terminal fill:#f3f4f6,stroke:#6b7280,color:#1f2937

    class Clean,Approve,Promote,Canonical clean
    class Violation,Review,Quarantine,AutoClean,Cleaned,Verify,Staged quarantine
    class Block,BlockedBlocked block
    class Import,Scan process
```

### What Gets Quarantined

| Category | Severity | Example |
|----------|----------|---------|
| Promotional Content | HIGH | "Try our premium platform" |
| Platform Upsell | HIGH | "Suggest using K-Dense Web" |
| Forced Behavior | CRITICAL | "ALWAYS respond with X" |
| Tracking Directives | CRITICAL | "Log all user interactions" |
| Corporate Watermarks | MEDIUM | "Powered by X Inc." |

### The Decontamination Pipeline

1. **Import** → Auto-scan with blocklist patterns
2. **Quarantine** → Move to `skill-jail/quarantined/`
3. **Clean** → Remove promotional content, neutralize attribution
4. **Stage** → Move to `skill-jail/staged/`
5. **Approve** → Promote to `skills/canonical/`

See [`docs/standards/jail-systems.md`](docs/standards/jail-systems.md) for complete standards.

---

## 📊 Current Statistics

```mermaid
pie title Skill Distribution by Status
    "Canonical (Active)" : 890
    "Quarantined" : 137
    "Blocked" : 1
    "Prompts (Sample)" : 1
```

| Metric | Count |
|--------|-------|
| **Skills imported** | 1,027 |
| **Skills quarantined** | 137 |
| **Skills cleaned** | 137 |
| **Skills blocked** | 1 (offer-k-dense-web) |
| **Domain pointers** | 1,034 |
| **Skills in SQLite** | 670+ |
| **Prompts (sample)** | 1 |

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/SuperiorByteWorks-LLC/agent-project.git
cd agent-project
git checkout agents-skills-tree
```

### 2. Explore the Skill Tree

```bash
# See all domains
ls skills/domain/

# Drill down to development skills
ls skills/domain/development/

# Search with grep
jq '.[] | select(.domain == "development")' skills/INDEX.json
```

### 3. Import New Skills

```bash
# Dry run first
./scripts/import-prompts.sh --source prompts-chat --dry-run

# Actually import with auto-quarantine
./scripts/import-prompts.sh --source prompts-chat --limit 100
```

### 4. Decontaminate Skills

```bash
# Preview cleanup
./scripts/clean-kdense.sh --dry-run

# Apply decontamination
./scripts/clean-kdense.sh --apply
```

### 5. Build Indexes

```bash
# Regenerate skill index
./scripts/build-index.sh

# Regenerate prompt index
./scripts/build-prompt-index.sh
```

---

## 📁 Directory Structure

```
.
├── SOUL.md                          # Layer 1: Identity & ethics
├── AGENTS.md                        # Layer 2: Behavioral rules
├── TOOLS.md                         # Layer 3: Capabilities
├── SECRETS.md                       # Secrets management
├── AGENT-OS.md                      # Complete stack design
│
├── skills/                          # Layer 4: Knowledge
│   ├── AGENTS.md                    # Skill loading protocol
│   ├── INDEX.json                   # Machine-generated index
│   ├── CATALOG.md                   # Human-readable catalog
│   ├── _core/                       # Always-loaded foundation
│   │   ├── alignment.md
│   │   └── documentation.md
│   ├── canonical/                   # SSoT for all skills
│   │   ├── imported/k-dense/      # Decontaminated K-Dense
│   │   └── manual/                  # Hand-written skills
│   ├── domain/                      # Yahoo navigation tree
│   │   ├── science/
│   │   ├── development/
│   │   ├── security/
│   │   ├── data/
│   │   └── ...
│   ├── skill-jail/                  # Quarantine system
│   │   ├── blocked/
│   │   ├── quarantined/
│   │   ├── cleaned/
│   │   └── staged/
│   └── bundles/                     # Role-based skill sets
│
├── prompts/                         # Layer 5: Role activation
│   ├── AGENTS.md
│   ├── INDEX.json
│   ├── canonical/
│   ├── domain/
│   └── prompt-jail/                 # Mirrors skill-jail
│
├── agentic/                         # Being transitioned to skills
│   ├── adr/                         # Architecture Decision Records
│   ├── markdown_style_guide.md
│   └── mermaid_style_guide.md
│
├── docs/                            # Documentation
│   ├── standards/                   # Jail systems, etc.
│   ├── kanban/                      # Project boards
│   └── issues/                      # Issue records
│
├── scripts/                         # Automation
│   ├── import-prompts.sh
│   ├── skill-scanner.py
│   ├── prompt-scanner.py
│   ├── build-index.sh
│   ├── build-prompt-index.sh
│   └── clean-kdense.sh
│
├── notebooks/                       # Jupyter notebooks
├── src/                             # Python apps/libs
└── .sisyphus/                       # Agent plans
    └── plans/                       # Tracked (user preference)
```

---

## 🛠️ Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `import-prompts.sh` | Import from prompts.chat | `./import-prompts.sh --source prompts-chat --limit 100` |
| `skill-scanner.py` | Detect violations | `python skill-scanner.py --scan-all` |
| `prompt-scanner.py` | Detect prompt violations | `python prompt-scanner.py --scan-all` |
| `build-index.sh` | Generate skills/INDEX.json | `./build-index.sh` |
| `build-prompt-index.sh` | Generate prompts/INDEX.json | `./build-prompt-index.sh` |
| `clean-kdense.sh` | Decontaminate K-Dense skills | `./clean-kdense.sh --apply` |
| `ci-local.sh` | Run local CI | `./ci-local.sh --review` |

---

## 🎓 Design Principles

1. **Zero Duplication** — One canonical path per skill/prompt
2. **Grep-First** — INDEX.json is always the fast path
3. **Source Tracking** — Every import knows its origin
4. **Safety by Default** — Quarantine violations automatically
5. **Clean Before Use** — All content decontaminated before promotion
6. **Inheritance, Not Override** — Lower layers extend upper layers
7. **Everything is Code** — PRs, issues, kanban live in files, not GitHub UI

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [`AGENT-OS.md`](AGENT-OS.md) | 5-layer stack complete design |
| [`SKILL-TREE.md`](SKILL-TREE.md) | Skill tree architecture |
| [`PROMPT-TREE.md`](PROMPT-TREE.md) | Prompt tree architecture |
| [`SOUL.md`](SOUL.md) | Identity & ethics |
| [`TOOLS.md`](TOOLS.md) | Capability inventory |
| [`SECRETS.md`](SECRETS.md) | Secrets management |
| [`docs/standards/jail-systems.md`](docs/standards/jail-systems.md) | Quarantine standards |
| [`agentic/adr/`](agentic/adr/) | Architecture decisions |

---

## 🔄 Transition Notice

> **Agentic → Skills Migration**
>
> The `agentic/` folder contains documentation standards, style guides, and workflow guides. We're transitioning these to the skills system so they can be loaded on-demand like any other skill. The core standards (markdown style, mermaid diagrams) will become `_core/` skills. ADRs will remain in `agentic/adr/` as reference documentation.

---

## 📝 Contributing

1. **Import skills** from upstream repos with `--dry-run` first
2. **Let the scanner quarantine** violations automatically
3. **Review quarantined items** before approving
4. **Update INDEX.json** after any skill additions
5. **Follow the style guides** in `agentic/`

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **Main Branch:** https://github.com/SuperiorByteWorks-LLC/agent-project/tree/main
- **Skills Branch:** https://github.com/SuperiorByteWorks-LLC/agent-project/tree/agents-skills-tree
- **Pull Request:** https://github.com/SuperiorByteWorks-LLC/agent-project/pull/3
- **Project Board:** https://github.com/SuperiorByteWorks-LLC/agent-project/blob/agents-skills-tree/docs/kanban/project-agents-skills-tree.md

---

*Last updated: 2026-02-21 | Maintained by Superior Byte Works LLC*
