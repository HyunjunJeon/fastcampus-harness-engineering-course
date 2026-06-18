import * as os from "node:os";
import * as path from "node:path";

export const GJC_MANAGED_CODEX_HOOK_EVENTS = ["UserPromptSubmit", "Stop"] as const;

export type GjcManagedCodexHookEvent = (typeof GJC_MANAGED_CODEX_HOOK_EVENTS)[number];

type JsonObject = Record<string, unknown>;

export interface CodexCommandHook {
	type: "command";
	command: string;
	statusMessage?: string;
	timeout?: number;
}

export interface CodexHookEntry {
	hooks: CodexCommandHook[];
}

export interface GjcManagedCodexHooksConfig {
	hooks: Record<GjcManagedCodexHookEvent, CodexHookEntry[]>;
}

export interface MergeGjcManagedCodexHooksResult {
	content: string;
	changed: boolean;
	managedHookCount: number;
}

export interface GjcCodexHooksStatus {
	hooksPath: string;
	installed: boolean;
	missingEvents: GjcManagedCodexHookEvent[];
	managedHookCount: number;
}

function isJsonObject(value: unknown): value is JsonObject {
	return typeof value === "object" && value !== null && !Array.isArray(value);
}

function normalizeHooksRoot(parsed: unknown): JsonObject {
	if (!isJsonObject(parsed)) return {};
	return structuredClone(parsed);
}

function normalizeHooksMap(root: JsonObject): Record<string, unknown> {
	if (isJsonObject(root.hooks)) return root.hooks;
	const hooks: Record<string, unknown> = {};
	root.hooks = hooks;
	return hooks;
}

function commandIsGjcManaged(value: unknown): boolean {
	if (typeof value !== "string") return false;
	return /\bgjc(?:\.exe)?\b/.test(value) && /\bcodex-native-hook\b/.test(value);
}

function entryContainsGjcManagedHook(value: unknown): boolean {
	if (!isJsonObject(value) || !Array.isArray(value.hooks)) return false;
	return value.hooks.some(hook => isJsonObject(hook) && commandIsGjcManaged(hook.command));
}

function managedCommand(): string {
	return "gjc codex-native-hook";
}

function managedEntry(event: GjcManagedCodexHookEvent): CodexHookEntry {
	const hook: CodexCommandHook = {
		type: "command",
		command: managedCommand(),
		statusMessage: "GJC skill state",
		...(event === "Stop" ? { timeout: 30 } : {}),
	};
	return { hooks: [hook] };
}

export function buildGjcManagedCodexHooksConfig(): GjcManagedCodexHooksConfig {
	return {
		hooks: {
			UserPromptSubmit: [managedEntry("UserPromptSubmit")],
			Stop: [managedEntry("Stop")],
		},
	};
}

export function getDefaultCodexHooksPath(homeDir = os.homedir()): string {
	return path.join(homeDir, ".codex", "hooks.json");
}

export function mergeGjcManagedCodexHooksConfig(existingContent: string | null): MergeGjcManagedCodexHooksResult {
	let root = normalizeHooksRoot(null);
	if (existingContent?.trim()) {
		try {
			root = normalizeHooksRoot(JSON.parse(existingContent) as unknown);
		} catch {
			root = normalizeHooksRoot(null);
		}
	}

	const hooks = normalizeHooksMap(root);
	const managed = buildGjcManagedCodexHooksConfig();
	let managedHookCount = 0;

	for (const event of GJC_MANAGED_CODEX_HOOK_EVENTS) {
		const existingEntries = Array.isArray(hooks[event]) ? hooks[event] : [];
		const userEntries = existingEntries.filter(entry => !entryContainsGjcManagedHook(entry));
		const nextEntries = [...managed.hooks[event], ...userEntries];
		managedHookCount += managed.hooks[event].length;
		hooks[event] = nextEntries;
	}

	const content = `${JSON.stringify(root, null, 2)}\n`;
	return { content, changed: content !== (existingContent ?? ""), managedHookCount };
}

export function readGjcManagedCodexHooksStatus(content: string | null, hooksPath: string): GjcCodexHooksStatus {
	const missingEvents: GjcManagedCodexHookEvent[] = [];
	let managedHookCount = 0;
	let hooks: Record<string, unknown> = {};
	if (content?.trim()) {
		try {
			const root = normalizeHooksRoot(JSON.parse(content) as unknown);
			hooks = isJsonObject(root.hooks) ? root.hooks : {};
		} catch {
			hooks = {};
		}
	}

	for (const event of GJC_MANAGED_CODEX_HOOK_EVENTS) {
		const entries = Array.isArray(hooks[event]) ? hooks[event] : [];
		const eventManagedCount = entries.filter(entryContainsGjcManagedHook).length;
		managedHookCount += eventManagedCount;
		if (eventManagedCount === 0) missingEvents.push(event);
	}

	return {
		hooksPath,
		installed: missingEvents.length === 0,
		missingEvents,
		managedHookCount,
	};
}
