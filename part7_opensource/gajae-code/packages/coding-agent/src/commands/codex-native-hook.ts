import { Command } from "@gajae-code/utils/cli";
import { runGjcNativeSkillHookCli } from "../hooks/native-skill-hook";

export default class CodexNativeHook extends Command {
	static description = "Run GJC native UserPromptSubmit/Stop skill-state hook";
	static strict = false;

	async run(): Promise<void> {
		await runGjcNativeSkillHookCli();
	}
}
