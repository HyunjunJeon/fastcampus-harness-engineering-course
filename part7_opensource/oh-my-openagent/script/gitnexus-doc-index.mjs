#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs"
import { join, relative } from "node:path"
import { pathToFileURL } from "node:url"

const REPO_ROOT = process.cwd()
const WIKI_DIR = join(REPO_ROOT, ".gitnexus", "wiki")
const DOC_SLUG = "documentation-index"
const DOC_TITLE = "Documentation Index"

const ROOT_DOCS = [
  "AGENTS.md",
  "README.ko.md",
  "README.md",
  "ANALYSIS.ko.md",
  "ARCHITECTURE.md",
  "CONTRIBUTING.md",
  "ROADMAP.md",
  "CHANGELOG.md",
  ".agents/AGENTS.md",
  "packages/AGENTS.md",
  "script/AGENTS.md",
]

const DOC_GROUPS = [
  {
    heading: "Root Orientation",
    paths: ROOT_DOCS,
  },
  {
    heading: "User Documentation",
    paths: listMarkdownUnder("docs"),
  },
  {
    heading: "Package Guidance",
    paths: listFilesByName("packages", "AGENTS.md"),
  },
  {
    heading: "GitNexus Reports",
    paths: listMarkdownUnder(".omo/reports/20260618-gitnexus-oh-my-openagent"),
  },
]

function listMarkdownUnder(dir) {
  return listFiles(dir).filter((path) => path.endsWith(".md"))
}

function listFilesByName(dir, filename) {
  return listFiles(dir).filter((path) => path.endsWith(`/${filename}`) || path === filename)
}

function listFiles(dir) {
  const root = join(REPO_ROOT, dir)
  if (!existsSync(root)) return []
  const output = []
  const stack = [root]
  while (stack.length > 0) {
    const current = stack.pop()
    const entries = readdirSync(current, { withFileTypes: true })
      .filter((entry) => !shouldSkip(entry.name))
      .sort((a, b) => a.name.localeCompare(b.name))
    for (const entry of entries) {
      const absolute = join(current, entry.name)
      if (entry.isDirectory()) {
        stack.push(absolute)
      } else if (entry.isFile()) {
        output.push(toRepoPath(absolute))
      }
    }
  }
  return output.sort()
}

function shouldSkip(name) {
  return name === "node_modules" || name === "dist" || name === ".git" || name === ".gitnexus"
}

function toRepoPath(absolutePath) {
  return relative(REPO_ROOT, absolutePath).replaceAll("\\", "/")
}

function uniqueExisting(paths) {
  return Array.from(new Set(paths)).filter((path) => existsSync(join(REPO_ROOT, path))).sort()
}

function buildMarkdown(groups) {
  const lines = [
    "# Documentation Index",
    "",
    "GitNexus source wiki는 코드 실행 그래프를 중심으로 생성됩니다. 이 페이지는 코드 그래프에 잘 드러나지 않는 프로젝트 문서와 학습용 분석 문서를 함께 찾기 위한 보조 인덱스입니다.",
    "",
    `Generated: ${new Date().toISOString()}`,
    "",
  ]
  for (const group of groups) {
    const paths = uniqueExisting(group.paths)
    if (paths.length === 0) continue
    lines.push(`## ${group.heading}`, "")
    for (const path of paths) {
      lines.push(`- [${path}](${pathToFileURL(join(REPO_ROOT, path)).href})`)
    }
    lines.push("")
  }
  return `${lines.join("\n").trimEnd()}\n`
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"))
}

function writeJson(path, value) {
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`)
}

function upsertDocumentationNode(tree, files) {
  const next = Array.isArray(tree) ? tree.filter((node) => node.slug !== DOC_SLUG) : []
  next.push({
    name: DOC_TITLE,
    slug: DOC_SLUG,
    files,
    children: [],
  })
  return next
}

function updateModuleTrees(files) {
  const names = [
    "module_tree.json",
    "module_tree.source-only.json",
    "module_tree.source-only-curated.json",
  ]
  for (const name of names) {
    const path = join(WIKI_DIR, name)
    if (!existsSync(path)) continue
    writeJson(path, upsertDocumentationNode(readJson(path), files))
  }
}

function updateMeta(files) {
  const path = join(WIKI_DIR, "meta.json")
  if (!existsSync(path)) return
  const meta = readJson(path)
  meta.moduleFiles = {
    ...(meta.moduleFiles ?? {}),
    [DOC_TITLE]: files,
  }
  meta.moduleTree = upsertDocumentationNode(meta.moduleTree ?? [], files)
  meta.documentationIndexGeneratedAt = new Date().toISOString()
  writeJson(path, meta)
}

function updateOverview() {
  const path = join(WIKI_DIR, "overview.md")
  if (!existsSync(path)) return
  const marker = "## 문서 인덱스"
  const current = readFileSync(path, "utf8")
  const block = [
    marker,
    "",
    "코드 그래프에 포함되지 않는 프로젝트 문서 목록은 [Documentation Index](documentation-index.md)에서 함께 확인합니다.",
    "",
  ].join("\n")
  if (current.includes(marker)) return
  writeFileSync(path, `${current.trimEnd()}\n\n${block}`)
}

function readHtmlAssignment(html, name) {
  const prefix = `var ${name} = `
  const start = html.indexOf(prefix)
  if (start === -1) return null
  const jsonStart = start + prefix.length
  const end = html.indexOf(";\n", jsonStart)
  if (end === -1) return null
  return {
    start,
    end: end + 2,
    value: JSON.parse(html.slice(jsonStart, end)),
  }
}

function replaceHtmlAssignment(html, name, value) {
  const assignment = readHtmlAssignment(html, name)
  if (!assignment) return html
  const next = `var ${name} = ${JSON.stringify(value)};\n`
  return `${html.slice(0, assignment.start)}${next}${html.slice(assignment.end)}`
}

function updateHtml(markdown, files) {
  const path = join(WIKI_DIR, "index.html")
  if (!existsSync(path)) return
  let html = readFileSync(path, "utf8")
  const pages = readHtmlAssignment(html, "PAGES")?.value
  const tree = readHtmlAssignment(html, "TREE")?.value
  const meta = readHtmlAssignment(html, "META")?.value
  if (pages) {
    pages[DOC_SLUG] = markdown
    html = replaceHtmlAssignment(html, "PAGES", pages)
  }
  if (tree) {
    html = replaceHtmlAssignment(html, "TREE", upsertDocumentationNode(tree, files))
  }
  if (meta) {
    meta.moduleFiles = {
      ...(meta.moduleFiles ?? {}),
      [DOC_TITLE]: files,
    }
    meta.moduleTree = upsertDocumentationNode(meta.moduleTree ?? [], files)
    meta.documentationIndexGeneratedAt = new Date().toISOString()
    html = replaceHtmlAssignment(html, "META", meta)
  }
  writeFileSync(path, html)
}

function main() {
  if (!existsSync(WIKI_DIR) || !statSync(WIKI_DIR).isDirectory()) {
    throw new Error(".gitnexus/wiki does not exist. Run `node .gitnexus/run.cjs wiki ...` first.")
  }

  const groups = DOC_GROUPS.map((group) => ({
    ...group,
    paths: uniqueExisting(group.paths),
  })).filter((group) => group.paths.length > 0)
  const files = uniqueExisting(groups.flatMap((group) => group.paths))
  const markdown = buildMarkdown(groups)

  writeFileSync(join(WIKI_DIR, `${DOC_SLUG}.md`), markdown)
  updateModuleTrees(files)
  updateMeta(files)
  updateOverview()
  updateHtml(markdown, files)

  console.log(`GitNexus documentation index updated: ${files.length} files`)
}

main()
