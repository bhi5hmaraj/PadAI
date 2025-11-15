# Beads JSONL → React Flow Visualizer

Visualize a Beads JSONL export as a DAG with React Flow and Dagre.

## Features
- Parse JSONL (LF/CRLF safe)
- DAG layout from **blocks** edges; **related** edges dotted and can nudge ordering
- Top-down or left-right orientation
- Status color scheme; hover highlights neighbors without flicker
- Search + status filters
- Group all isolated nodes into a bucket; click to fan out temporarily
- Built-in self-tests (parser + layout safety)

## Quickstart
```bash
pnpm i   # or npm i / yarn
pnpm dev # or npm run dev
```

Then open the local URL Vite prints. Load your `.jsonl` or click **Load demo**.

## Notes
- Tailwind is optional. We use utility-like class names but the UI works fine without Tailwind.
- If you want Tailwind styles, add Tailwind to the project as usual.
