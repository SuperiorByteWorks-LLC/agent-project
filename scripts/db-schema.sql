-- SQLite schema for skills database
-- Generated from canonical/ skills

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    canonical_path TEXT NOT NULL,
    description TEXT,
    domain TEXT,
    subdomain TEXT,
    tags TEXT,
    bundles TEXT,
    upstream_url TEXT,
    license TEXT,
    import_date TEXT,
    import_commit TEXT,
    content_hash TEXT,
    load_frequency TEXT,
    skill_author TEXT,
    search_text TEXT
);

CREATE INDEX idx_name ON skills(name);
CREATE INDEX idx_domain ON skills(domain);
CREATE INDEX idx_tags ON skills(tags);

-- Full-text search using FTS5
CREATE VIRTUAL TABLE skills_fts USING fts5(
    name,
    description,
    search_text,
    content='skills',
    content_rowid='id'
);

-- Pointers table for domain navigation
CREATE TABLE pointers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER REFERENCES skills(id),
    domain TEXT,
    subdomain TEXT,
    pointer_path TEXT
);

CREATE INDEX idx_pointers_domain ON pointers(domain, subdomain);

-- Version tracking
CREATE TABLE db_version (
    commit_hash TEXT PRIMARY KEY,
    built_at TEXT,
    skill_count INTEGER
);
