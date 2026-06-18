import { describe, expect, it } from "bun:test";
import * as path from "node:path";

const repoRoot = path.resolve(import.meta.dir, "..", "..", "..");
const agentsEntry = path.join(repoRoot, "packages", "coding-agent", "src", "task", "agents.ts");
const promptsDir = path.join(repoRoot, "packages", "coding-agent", "src", "prompts", "agents");

function extractEmbeddedAgentFileNames(source: string): string[] {
	const defsBlock = source.match(/const EMBEDDED_AGENT_DEFS: EmbeddedAgentDef\[\] = \[([\s\S]*?)\];/);
	if (!defsBlock) return [];
	return [...defsBlock[1].matchAll(/fileName: "([^"]+)"/g)].map(match => match[1]).sort();
}

describe("GJC bundled task agent surface", () => {
	it("ships four visible role agents plus retained hidden support agents", async () => {
		const source = await Bun.file(agentsEntry).text();
		expect(extractEmbeddedAgentFileNames(source)).toEqual([
			"architect.md",
			"critic.md",
			"executor.md",
			"explore.md",
			"plan.md",
			"planner.md",
			"reviewer.md",
			"task.md",
		]);

		const promptFiles = Array.from(new Bun.Glob("*.md").scanSync({ cwd: promptsDir })).sort();
		expect(promptFiles).toEqual([
			"architect.md",
			"critic.md",
			"executor.md",
			"explore.md",
			"frontmatter.md",
			"init.md",
			"plan.md",
			"planner.md",
			"reviewer.md",
			"task.md",
		]);
	});
});
