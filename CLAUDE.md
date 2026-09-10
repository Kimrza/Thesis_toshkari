## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules (each `graphify <verb>` rule applies ONLY when a `graphify` CLI executable is
installed and on PATH — on clones without it, the graph outputs under graphify-out/ are
still readable, the `/graphify` skill (`.claude/skills/graphify/SKILL.md`) remains the
way to rebuild or update the graph, and direct file reads/greps are the sanctioned
fallback; verified 2026-09-10: no such executable exists on this clone):
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists and the CLI is installed. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` (CLI installed) or `/graphify <path> --update` (skill) to keep the graph current (AST-only, no API cost); when neither is available, note that the graph is stale for the touched files.
