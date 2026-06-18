# GitNexus database (download required)

This folder ships the GitNexus **navigation artifacts** (`wiki/`, `meta.json`,
`run.cjs`) so you can read the generated code map right away. The heavy pieces are
kept out of git on purpose:

| Item | Size | In git? | How to get it |
|------|------|---------|---------------|
| `lbug` (graph database) | ~233MB | No (> GitHub 100MB limit) | `./fetch-db.sh` (GitHub Release) |
| `parse-cache/`, `parsedfile-cache/` | ~223MB | No | optional; `node .gitnexus/run.cjs analyze` |
| `wiki/`, `meta.json`, `run.cjs` | small | Yes | already here |

## Get the database without re-running the AI

```sh
cd .gitnexus
./fetch-db.sh
```

This pulls the prebuilt `lbug` database from the repo's GitHub Release
(`gitnexus-db-v1`). Once it lands, the GitNexus MCP tools (`query`, `impact`,
`context`, ...) work against the same index used to build this course — no paid
re-analysis needed.

Windows without a POSIX shell? Download it directly:
<https://github.com/HyunjunJeon/fastcampus-harness-engineering-course/releases/download/gitnexus-db-v1/oh-my-openagent-lbug>
and save it as `.gitnexus/lbug`.
