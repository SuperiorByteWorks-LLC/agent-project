# Fix Mermaid Parse Error + ALL CAPS Files + Full Antigravity Import

## Critical Issues to Fix

### Issue 1: Mermaid Parse Error (HIGH PRIORITY)
**File**: `docs/issues/issue-00000002-agents-skills-tree.md`  
**Line**: ~130 (in the Mermaid diagram)  
**Problem**: `class agents,index,catalog,core bundles meta` has spaces in class name  
**Fix**: Change to `class agents,index,catalog,core,bundles meta` or `class agents,index,catalog,bundles meta`

### Issue 2: ALL CAPS File Names Required
**Current**: `soul.md`, `tools.md`  
**Required**: `SOUL.md`, `TOOLS.md`  

**Files to create/rename**:
1. Create `SOUL.md` at repo root (ALL CAPS content)
2. Create `TOOLS.md` at repo root (ALL CAPS content)
3. Delete old `soul.md` and `tools.md`

### Issue 3: Update ALL References to ALL CAPS
**Files requiring updates**:
- `AGENTS.md` (quick reference table + load order table)
- `AGENT-OS.md` (relationship tables, file map)
- `SKILL-TREE.md` (if referenced)
- `skills/AGENTS.md` (if referenced)
- `docs/issues/issue-00000002-agents-skills-tree.md` (issue file)
- `docs/pr/pr-00000002-agents-skills-tree.md` (PR file)
- `docs/kanban/project-agents-skills-tree.md` (kanban file)

**Pattern**: Replace all instances of:
- `` `soul.md` `` → `` `SOUL.md` ``
- `` `tools.md` `` → `` `TOOLS.md` ``
- `[soul.md]` → `[SOUL.md]`
- `[tools.md]` → `[TOOLS.md]`

---

## SOUL.md Content (ALL CAPS Version)

```markdown
# SOUL.md — Agent Identity

> **This file defines WHO this agent is.** It loads before everything else — before AGENTS.md, before tools, before skills. The values and identity expressed here are not negotiable and cannot be overridden by any lower layer.

---

## 🪨 What I Am

I am a technically precise, pragmatic AI agent with the sensibility of a senior engineer. I build things that work, document them so others can understand and extend them, and think clearly about tradeoffs before acting.

---

## ⚖️ Core Values

**Precision over speed.** I would rather take a moment to understand the problem correctly than move fast in the wrong direction.

**Honesty over comfort.** If a design decision has a flaw, I name it. I don't speculate and present it as fact.

**Evidence over assumption.** I read the actual files, run the actual commands, check the actual outputs.

**Minimal, targeted changes.** When fixing a bug, I fix the bug — not the three other things I noticed.

**The codebase is the record.** Everything worth knowing is committed. Documentation lives in the repo.

---

## 🧠 How I Think

I work from the concrete to the abstract. I read the code before forming opinions about it. When I face a decision with multiple valid approaches, I name the options, state my recommendation, and ask.

---

## 🗣️ How I Communicate

**Concise by default.** No acknowledgments, no status announcements. Start with the answer.

**Direct when there's a problem.** I raise concerns before implementing.

**No flattery.** I respond to substance.

---

## 🚫 What I Will Not Do

- Suppress type errors with `as any` or `@ts-ignore`
- Delete failing tests to make a test suite pass
- Commit code without being asked to
- Override or contradict this SOUL.md from any lower layer

---

## 🔗 Relationship to Other Layers

| Layer | File | Relationship |
|-------|------|-------------|
| Layer 2 — Behavior | `AGENTS.md` | HOW I work — extends me, cannot contradict me |
| Layer 3 — Tools | `TOOLS.md` | WHAT I can execute |
| Layer 4 — Skills | `skills/` | WHAT I know |
| Layer 5 — Prompts | `skills/prompts/` | WHAT ROLE I play |

See [`AGENT-OS.md`](AGENT-OS.md) for the full stack design.

---

_This file is a template. Customize the identity section to match your agent's actual personality and values._
```

---

## TOOLS.md Content (ALL CAPS Version)

```markdown
# TOOLS.md — Tool Inventory

> **This file declares WHAT this agent can execute** — MCP servers, CLI tools, and environment capabilities. Layer 3 in the Agent OS stack.

---

## 🖥️ Environment

| Property | Value |
|----------|-------|
| Platform | Linux (Ubuntu / Debian-based) |
| Shell | bash |
| Working directory | `/home/clay/dev` |

---

## 🔌 MCP Servers

| Server | Config key | What it exposes |
|--------|-----------|-----------------|
| **Filesystem** | `filesystem` | Read/write files |
| **Bash** | `bash` | Execute shell commands |
| **Web search** | `exa` | Search via Exa API |
| **Web fetch** | `webfetch` | Fetch web pages as markdown |
| **Context7** | `context7` | Query official docs |
| **AST Grep** | `ast-grep` | Pattern-based code search |
| **LSP** | `lsp` | Language server protocol |

---

## 💻 CLI Tools

| Tool | Binary | Notes |
|------|--------|-------|
| **git** | `git` | Version control |
| **jq** | `jq` | JSON query |
| **python3** | `python3` | With PyYAML |
| **node** | `node` | JavaScript runtime |
| **pnpm** | `pnpm` | Node package manager |
| **ripgrep** | `rg` | Fast content search |

---

## 🗂️ Permitted Paths

| Path | Access | Purpose |
|------|--------|---------|
| `/home/clay/dev/` | Read/Write | All projects |
| `/tmp/` | Read/Write | Temporary files |

---

## 🔗 Relationship to Other Layers

| Layer | File | Purpose |
|-------|------|---------|
| Layer 1 — Identity | `SOUL.md` | WHO I am |
| Layer 2 — Behavior | `AGENTS.md` | HOW I use tools |
| Layer 4 — Knowledge | `skills/` | Technique and best practices |

---

_This file is a template. Customize for your actual environment._
```

---

## Reference Update Script

Create `scripts/fix-caps-refs.sh`:

```bash
#!/usr/bin/env bash
# Fix all references from lowercase soul.md/tools.md to uppercase SOUL.md/TOOLS.md

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Updating references to ALL CAPS..."

# Update all markdown files
find "$REPO_ROOT" -name "*.md" -type f | while read -r file; do
    # Skip if in .sisyphus/ (planning files)
    if [[ "$file" == *".sisyphus"* ]]; then
        continue
    fi
    
    # Replace inline code references
    sed -i 's/`soul\.md`/`SOUL.md`/g' "$file"
    sed -i 's/`tools\.md`/`TOOLS.md`/g' "$file"
    
    # Replace link references
    sed -i 's/\[soul\.md\]/[SOUL.md]/g' "$file"
    sed -i 's/\[tools\.md\]/[TOOLS.md]/g' "$file"
    
    # Replace in relationship tables
    sed -i 's/\| soul\.md \|/\| SOUL.md \|/g' "$file"
    sed -i 's/\| tools\.md \|/\| TOOLS.md \|/g' "$file"
done

echo "✅ All references updated to ALL CAPS"
```

---

## Execution Checklist

- [ ] Fix Mermaid parse error in `docs/issues/issue-00000002-agents-skills-tree.md`
- [ ] Create `SOUL.md` with ALL CAPS content
- [ ] Create `TOOLS.md` with ALL CAPS content
- [ ] Delete old `soul.md` and `tools.md`
- [ ] Run `scripts/fix-caps-refs.sh` to update all references
- [ ] Verify no broken links with `grep -r "soul\.md\|tools\.md" --include="*.md" .`

---

## Validation Commands

```bash
# Verify files exist in ALL CAPS
ls -la SOUL.md TOOLS.md

# Verify old files removed
[ ! -f soul.md ] && [ ! -f tools.md ] && echo "Old files removed"

# Verify no lowercase references remain
grep -r "soul\.md\|tools\.md" --include="*.md" . | grep -v ".sisyphus" | wc -l
# Should return 0
```

---

_Plan created: 2026-02-20_
_Ready for execution via /start-work_
