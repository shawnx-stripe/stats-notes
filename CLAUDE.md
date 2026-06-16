# Obsidian Vault: Sufficient Statistics

## Project Context
Personal knowledge vault for causal inference, econometrics, A/B testing,
and experimental design. Uses Obsidian with MOC (Map of Content) hub pages.

## Note Conventions
- **Frontmatter**: Every note MUST have: title, aliases (list), tags (list), updated (YYYY-MM-DD)
- **Structure**: # Title → > [!summary] → ## sections → optional ## Minimal code snippets → ## Related notes
- **Filenames**:
  - Acronyms with known expansions: `Full Name (ABBR).md` in Title Case
    (e.g., `Inverse Probability Weighting (IPW).md`, `Ordinary Least Squares (OLS).md`).
    The abbreviation and lowercase expansion must both be aliases.
  - Formal methods/proper nouns: Title Case (e.g., `Bayesian Testing.md`)
  - Generic concepts: lowercase (e.g., `propensity score.md`)
  - MOC hubs: `Topic Name (MOC).md`
- **Aliases**: Add all common abbreviations and alternative names
- **Tags**: Use existing taxonomy: moc, experimentation, ab-testing, causal-inference,
  econometrics, panel-data, time-series, ml, variance-reduction, sequential, etc.
- **Links**: Use Obsidian wikilinks, for example `Note Name` inside double
  square brackets. Never include `.md` extension in links.
- **Math**: Use `$$...$$` for display, `$...$` for inline. Standard LaTeX notation.
  Use `\operatorname{}` for named operators. Use `\text{}` for text in math.
- **Code blocks**: Include code only where it helps the note's purpose. Estimator,
  test, software, and workflow pages should include copy-ready snippets with real
  package function signatures. MOCs, pure concepts, assumptions, estimands, and
  reading notes may omit code. Keep "minimal" code to 1-2 snippets and about 40
  total lines unless the page is explicitly a workflow page.
- **Callouts**: Use Obsidian callout syntax: `> [!summary]`, `> [!warning]`,
  `> [!tip]`, `> [!check]`, `> [!example]`, `> [!note]`

## When Creating a New Note
1. Check if the topic already exists (search filenames and aliases)
2. Use the standard structure (frontmatter → summary → sections → code → related)
3. Link FROM at least one MOC page
4. Link TO related concepts using wikilinks
5. Set `updated:` to today's date
6. Add to the A-Z index of the appropriate MOC(s)

## When Reviewing Notes
- Verify math formulas against canonical references
- Check that code snippets are syntactically valid and use correct function signatures
- Ensure all wikilinks resolve to existing files or are documented as planned stubs
- Check that assumptions and diagnostics are complete for each method

## Link Graph Expectations

- Every content note should have at least one incoming link from a MOC or source note.
- Every new or major concept should link back to its parent MOC and nearby concepts.
- Use `## Related notes` only for existing linked notes.
- Use `## Potential future notes` only for non-linked plain-text wishlist items.

## Tooling

### Obsidian CLI
`obsidian` is in PATH. Obsidian must be running for CLI commands to work.
Key commands:

```bash
obsidian unresolved                  # all broken wikilinks (ground truth)
obsidian orphans                     # files with no incoming links
obsidian deadends                    # files with no outgoing links
obsidian aliases file="FILENAME"     # list a file's aliases
obsidian links file="FILENAME"       # outgoing links from a file
obsidian backlinks file="FILENAME"   # incoming links to a file
obsidian search query="TERM"         # vault-wide text search
obsidian tags                        # all tags with counts
obsidian properties file="FILENAME"  # inspect YAML frontmatter
```

Always prefer the CLI for link validation — it uses Obsidian's actual resolver
and is the authoritative source for what's broken vs. resolved.

### Repo audit

Use the lightweight audit script for checks outside Obsidian's resolver:

```bash
python3 scripts/audit_vault.py
```

The script checks frontmatter, summary callouts, `## Related notes`, malformed
wikilinks, alias collisions, short-note inventory, MOC coverage, and tracked
ignored files. Slash commands and editor hooks may exist in a personal setup,
but they are not tracked in this repository.

### Alias standardization
Every note MUST have comprehensive aliases to prevent broken links:
- The filename itself (case variants: lowercase, Title Case)
- Common abbreviations (e.g., `DiD`, `RDD`, `IV`, `ITT`)
- Full expansions (e.g., `difference-in-differences` for `Difference-in-Differences (DiD)`)
- Never add an alias that conflicts with another file's name or existing alias
