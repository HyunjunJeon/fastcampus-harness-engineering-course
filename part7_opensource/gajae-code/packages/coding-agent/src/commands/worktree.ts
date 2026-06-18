/**
 * List and clean up agent-managed git worktrees under `~/.gjc/wt`.
 */
import { Args, Command, Flags } from "@gajae-code/utils/cli";
import { clearWorktrees, listWorktrees } from "../cli/worktree-cli";

export default class Worktree extends Command {
	static description = "List or clear agent-managed git worktrees (~/.gjc/wt)";

	static aliases = ["wt"];

	static args = {
		// `list` (default) inspects the worktree dir; `clear` removes entries.
		// A positional action keeps `gjc worktree` (the no-arg form) useful.
		action: Args.string({
			description: "list (default) or clear",
			required: false,
			options: ["list", "clear"],
			default: "list",
		}),
	};

	static flags = {
		all: Flags.boolean({
			description: "Clear every entry, including live PR-checkout worktrees (clear)",
			default: false,
		}),
		"dry-run": Flags.boolean({
			char: "n",
			description: "Print what would be removed without touching the filesystem (clear)",
			default: false,
		}),
		json: Flags.boolean({ char: "j", description: "Emit machine-readable JSON", default: false }),
	};

	static examples = [
		"gjc worktree",
		"gjc worktree list --json",
		"gjc worktree clear",
		"gjc worktree clear --dry-run",
		"gjc worktree clear --all",
	];

	async run(): Promise<void> {
		const { args, flags } = await this.parse(Worktree);
		if (args.action === "clear") {
			await clearWorktrees({
				all: flags.all ?? false,
				dryRun: flags["dry-run"] ?? false,
				json: flags.json ?? false,
			});
			return;
		}
		await listWorktrees({ json: flags.json ?? false });
	}
}
