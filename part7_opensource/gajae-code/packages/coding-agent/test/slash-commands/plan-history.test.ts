import { describe, expect, it } from "bun:test";
import { BUILTIN_SLASH_COMMANDS_INTERNAL } from "../../src/slash-commands/builtin-registry";

describe("removed workflow slash command handlers", () => {
	it("does not register removed /plan handler", () => {
		expect(BUILTIN_SLASH_COMMANDS_INTERNAL.some(command => command.name === "plan")).toBe(false);
	});
});
