# Sufficient Statistics Vault

Personal Obsidian vault for causal inference, econometrics, A/B testing, and
experimental design. The vault uses MOC pages as navigation hubs and short
applied-reference notes for individual methods, assumptions, diagnostics, and
estimands.

## Maintenance checks

Use Obsidian's resolver as the source of truth for wikilinks:

```bash
obsidian unresolved total
obsidian orphans
obsidian deadends
```

Run the repo audit for checks that Obsidian does not cover:

```bash
python3 scripts/audit_vault.py
```

The audit checks frontmatter, summary callouts, related-note sections, malformed
wikilinks, alias collisions, short-note inventory, MOC coverage, and tracked
ignored files.

## Note conventions

- Every content note has YAML frontmatter with `title`, `aliases`, `tags`, and
  `updated`.
- Every content note starts with a `> [!summary]` callout.
- Use `## Related notes` for existing linked notes.
- Use plain text, not wikilinks, for wishlist topics that do not exist yet.
- Include code only where it helps the note's purpose. Keep minimal code to one
  or two short snippets unless the page is explicitly a workflow page.
- Avoid duplicate aliases. A note should not claim another note's filename or
  canonical alias.

See `CLAUDE.md` for agent-specific editing guidance.
