# Million-Skill Architecture: Scalable Agent Skill Repository

## The Vision

**Target**: 10,000 → 1,000,000+ skills  
**Query Time**: < 100ms (not 3 seconds)  
**Storage**: Distributed, sharded  
**Search**: Semantic + lexical + graph  
**No Duplication**: Content-addressed deduplication

---

## Current Bottlenecks (Why JSON Won't Scale)

| Scale | Current (JSON) | Required |
|-------|---------------|----------|
| 1,000 skills | 2MB INDEX.json | ✅ Works |
| 10,000 skills | 20MB INDEX.json | ⚠️ Slow |
| 100,000 skills | 200MB INDEX.json | ❌ Fails |
| 1,000,000 skills | 2GB INDEX.json | ❌ Impossible |

**Problems**:
- Linear scan O(n) - jq loads entire file
- No pagination
- No caching
- Single file bottleneck
- No concurrent access

---

## Phase 1: Distributed Storage Layer

### 1.1 Content-Addressed Storage (CAS)

```python
# Every skill content hashed → stored by hash
skill_content_hash = sha256(skill_content)
storage_path = f"cas/{skill_content_hash[:2]}/{skill_content_hash[2:4]}/{skill_content_hash}"
```

**Benefits**:
- Automatic deduplication (same content = same hash)
- Immutable history
- Distributed by design
- Verifiable integrity

### 1.2 Database Schema

```sql
-- skills table (metadata only, content in CAS)
CREATE TABLE skills (
    id UUID PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    content_hash CHAR(64) NOT NULL,
    canonical_path VARCHAR(512) NOT NULL,
    description TEXT,
    domain VARCHAR(64),
    subdomain VARCHAR(64),
    upstream_url VARCHAR(512),
    license VARCHAR(32),
    import_date TIMESTAMP,
    last_sync TIMESTAMP,
    version VARCHAR(32),
    -- For fast filtering
    tags TEXT[],
    compatible_agents TEXT[],
    -- For search
    search_vector TSVECTOR,
    -- For analytics
    load_count INTEGER DEFAULT 0,
    avg_load_time_ms FLOAT
);

-- Full-text search index
CREATE INDEX idx_skills_search ON skills USING GIN(search_vector);

-- Domain index for drill-down
CREATE INDEX idx_skills_domain ON skills(domain, subdomain);

-- Tag index
CREATE INDEX idx_skills_tags ON skills USING GIN(tags);

-- Hash index for dedup
CREATE INDEX idx_skills_hash ON skills(content_hash);

-- pointers table (taxonomy navigation)
CREATE TABLE pointers (
    id UUID PRIMARY KEY,
    skill_id UUID REFERENCES skills(id),
    domain VARCHAR(64),
    subdomain VARCHAR(64),
    pointer_path VARCHAR(512),
    UNIQUE(domain, subdomain, skill_id)
);

-- embeddings table (for semantic search)
CREATE TABLE skill_embeddings (
    skill_id UUID PRIMARY KEY REFERENCES skills(id),
    embedding VECTOR(1536),  -- OpenAI/Claude embedding
    description_embedding VECTOR(1536),
    what_it_does_embedding VECTOR(1536)
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON skill_embeddings USING hnsw (embedding vector_cosine_ops);
```

### 1.3 Sharding Strategy

```
Shard by domain prefix:
- shard_science: skills.domain LIKE 'science%'
- shard_development: skills.domain LIKE 'development%'
- shard_security: skills.domain LIKE 'security%'
- ...

Each shard:
- Separate database instance
- Own INDEX.json (local to shard)
- Cross-shard queries via coordinator
```

---

## Phase 2: Multi-Modal Search System

### 2.1 Three-Layer Search

```
┌─────────────────────────────────────────┐
│ Layer 3: Semantic Search                │
│ (Meaning, intent, context)              │
│ - Vector embeddings                     │
│ - Similarity matching                   │
│ - "Find skills like X"                  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ Layer 2: Full-Text Search               │
│ (Lexical, keywords)                     │
│ - PostgreSQL tsvector                   │
│ - Fuzzy matching                        │
│ - "Skills with 'typescript'"            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ Layer 1: Graph Navigation                 │
│ (Hierarchy, relationships)                │
│ - Domain tree traversal                 │
│ - Pointer following                     │
│ - "Browse development/languages"          │
└─────────────────────────────────────────┘
```

### 2.2 Query Routing

```python
class SkillQueryRouter:
    def route(self, query: str) -> SearchStrategy:
        # Analyze query
        if query.startswith('/') or 'domain/' in query:
            return GraphNavigationStrategy()
        
        if len(query) < 20 and not ' ' in query:
            return FullTextStrategy()  # Tag/single word
        
        if self.is_question(query) or 'how to' in query.lower():
            return SemanticStrategy()  # Intent-based
        
        # Hybrid: all three
        return HybridStrategy()
```

### 2.3 Semantic Search (The Game Changer)

```python
# Pre-compute embeddings for all skills
# Query: "how do I configure strict TypeScript"
# Matches: "typescript-expert" (not just keyword match)

async def semantic_search(query: str, limit: int = 10):
    # Embed query
    query_embedding = await embed_text(query)
    
    # Find similar skills
    results = await db.query("""
        SELECT s.*, 1 - (e.embedding <=> $1) as similarity
        FROM skill_embeddings e
        JOIN skills s ON e.skill_id = s.id
        ORDER BY e.embedding <=> $1
        LIMIT $2
    """, query_embedding, limit)
    
    return results
```

**Why this matters**:
- "Authentication" → matches "oauth2-flow", "jwt-handler", "login-system"
- Not just keyword matching — understands intent
- Scales to millions via vector indices (HNSW)

---

## Phase 3: Caching & Performance

### 3.1 Multi-Tier Caching

```
L1: In-memory (Redis/Memcached)
     - Hot skills (top 1000)
     - Query results (5 min TTL)
     
L2: Local disk
     - Recently accessed skills
     - INDEX.json shards
     
L3: CDN/Edge
     - Static skill content
     - Global distribution
     
L4: Database
     - Source of truth
```

### 3.2 Lazy Loading at Scale

```python
class SkillLoader:
    def __init__(self):
        self.cache = LRUCache(maxsize=10000)
        self.hot_skills = self.load_hot_list()  # Top 1K
    
    async def load(self, skill_id: UUID) -> Skill:
        # Check L1 cache
        if skill_id in self.cache:
            return self.cache[skill_id]
        
        # Check if hot skill (preloaded)
        if skill_id in self.hot_skills:
            skill = self.hot_skills[skill_id]
            self.cache[skill_id] = skill
            return skill
        
        # Fetch from DB
        skill = await db.get_skill(skill_id)
        self.cache[skill_id] = skill
        return skill
```

### 3.3 Predictive Preloading

```python
# Based on current session context, preload likely skills
async def preload_contextual_skills(task_type: str, domain: str):
    # Get skills commonly used together
    related = await db.query("""
        SELECT s2.* FROM skill_usage_patterns p
        JOIN skills s2 ON p.related_skill_id = s2.id
        WHERE p.primary_skill_domain = $1
        AND p.task_type = $2
        ORDER BY p.frequency DESC
        LIMIT 50
    """, domain, task_type)
    
    # Load into memory
    for skill in related:
        await loader.load(skill.id)
```

---

## Phase 4: Real-Time Index Updates

### 4.1 Event-Driven Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Upstream   │────▶│   Ingestor   │────▶│  Validator  │
│   Source    │     │   Service    │     │   Sandbox   │
└─────────────┘     └──────────────┘     └─────────────┘
                                                  │
┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
│   Query     │◀────│    Index     │◀────│    Store    │
│   Service   │     │   Updater    │     │   Service   │
└─────────────┘     └──────────────┘     └─────────────┘
```

### 4.2 Incremental Index Updates

```python
# Don't regenerate entire INDEX.json
# Update only changed shards

async def incremental_update(skill_changes: List[SkillChange]):
    for change in skill_changes:
        shard = get_shard(change.domain)
        
        if change.type == 'ADD':
            await shard.add_skill(change.skill)
        elif change.type == 'UPDATE':
            await shard.update_skill(change.skill)
        elif change.type == 'DELETE':
            await shard.remove_skill(change.skill_id)
        
        # Update search indices
        await search_index.update(change)
        await vector_index.update(change)
```

---

## Phase 5: Distributed Architecture

### 5.1 Microservices

```
┌─────────────────────────────────────────────┐
│              API Gateway                      │
│         (Rate limiting, auth)               │
└──────────┬──────────────┬───────────────────┘
           │              │
    ┌──────▼──────┐ ┌────▼──────┐
    │   Query     │ │  Ingest   │
    │   Service   │ │  Service  │
    └──────┬──────┘ └────┬──────┘
           │             │
    ┌──────▼──────┐ ┌────▼──────┐
    │   Search    │ │  Validate │
    │   Service   │ │  Service  │
    └──────┬──────┘ └────┬──────┘
           │             │
    ┌──────▼─────────────▼──────┐
    │      Data Layer           │
    │  (PostgreSQL + Redis + S3)│
    └───────────────────────────┘
```

### 5.2 Read Replicas

```
Primary DB (writes)
    │
    ├──▶ Read Replica 1 (US-East)
    ├──▶ Read Replica 2 (US-West)
    ├──▶ Read Replica 3 (EU-West)
    └──▶ Read Replica 4 (Asia-Pacific)

Query routing: Nearest replica
```

---

## Phase 6: Federation & Aggregation

### 6.1 Skill Federation Protocol

```yaml
# skills.yaml - Federation manifest
federation:
  version: "1.0"
  
  # Local skills
  local:
    path: ./skills/canonical/
    
  # Remote sources (other skill repos)
  remotes:
    - name: "antigravity"
      url: "https://skills.antigravity.io/registry.json"
      sync_interval: "1h"
      
    - name: "kdense"
      url: "https://skills.kdense.ai/v1/registry"
      sync_interval: "24h"
      
    - name: "ghostsecurity"
      url: "https://skills.ghostsecurity.io/feed"
      sync_interval: "1d"
  
  # Aggregation strategy
  aggregation:
    deduplicate_by: "content_hash"
    prefer_local: true
    conflict_resolution: "upstream_timestamp"
```

### 6.2 Distributed Search

```python
# Search across multiple federated sources
async def federated_search(query: str):
    # Search local index
    local_results = await local_search(query)
    
    # Search remote indexes (parallel)
    remote_tasks = [
        remote.search(query) 
        for remote in federated_sources
    ]
    remote_results = await asyncio.gather(*remote_tasks)
    
    # Merge and deduplicate
    all_results = merge_results([local_results] + remote_results)
    
    # Re-rank by relevance
    return rerank(all_results, query)
```

---

## Implementation Roadmap

### MVP (Now): 1,000 skills
- JSON-based (current)
- Single file INDEX.json
- jq-based search

### Phase 1 (Month 1): 10,000 skills
- SQLite backend
- Local search indices
- File-based storage

### Phase 2 (Month 2): 100,000 skills
- PostgreSQL
- Full-text search (tsvector)
- Sharded INDEX.json

### Phase 3 (Month 3): 1,000,000 skills
- PostgreSQL + pgvector
- Semantic search
- Redis caching
- Read replicas

### Phase 4 (Month 6): 10,000,000+ skills
- Distributed architecture
- Microservices
- Federation protocol
- CDN distribution

---

## Technical Decisions

### Why PostgreSQL over Elasticsearch?

| Feature | PostgreSQL | Elasticsearch |
|---------|-----------|----------------|
| Full-text | ✅ | ✅ |
| Vectors (pgvector) | ✅ | ✅ |
| ACID | ✅ | ❌ |
| JSON | ✅ | ✅ |
| Maturity | 30+ years | 10 years |
| Complexity | Low | High |

**Decision**: Start with PostgreSQL. Can add Elasticsearch later if needed.

### Why Content-Addressed Storage?

- **Deduplication**: Same content = same hash
- **Integrity**: Verify content hasn't changed
- **Distribution**: Hash determines location
- **Caching**: Immutable = infinite cache

### Why Not Just Use SkillKit?

SkillKit is a **package manager**. We need a **search engine + registry**.

- SkillKit: `skillkit install <skill>` (pull)
- Our system: `search("typescript authentication")` (query)

**Complementary**: Use SkillKit for distribution, our system for discovery.

---

## Performance Targets

| Metric | Current | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|---------|
| Skills | 1K | 10K | 100K | 1M+ |
| Query Time | 2s | 500ms | 100ms | 50ms |
| Storage | 2MB | 20MB | 200MB | 2GB+ |
| Concurrency | 1 | 10 | 100 | 1000+ |
| Search Types | Lexical | Lexical | Lexical+Graph | Lexical+Graph+Semantic |

---

## Migration Path

```bash
# Step 1: Dual mode (JSON + DB)
./scripts/migrate/to-sqlite.sh

# Step 2: Parallel running
./scripts/serve/dual-mode.py  # Both APIs

# Step 3: Cutover
./scripts/migrate/cutover.sh

# Step 4: Clean up
rm skills/INDEX.json  # Now in DB
```

---

## Query Examples (Target)

```bash
# Current (jq)
jq '.[] | select(.tags | contains("typescript"))' skills/INDEX.json  # 2s

# Phase 1 (SQLite)
skill-query --tag=typescript  # 500ms

# Phase 2 (GraphQL)
skill-query "domain:development AND tags:typescript"  # 100ms

# Phase 3 (Semantic)
skill-query "how to configure strict TypeScript"  # 50ms
# Returns: typescript-expert, tsconfig-strict, type-guards

# Phase 4 (Federated)
skill-query "secure authentication patterns"  # 50ms
# Searches: local + antigravity + kdense + ghostsecurity
# Returns: unified, ranked results
```

---

_This architecture scales from 1,000 to 1,000,000+ skills._
_Endgame: The definitive skill discovery platform._
