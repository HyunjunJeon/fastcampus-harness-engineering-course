import { describe, expect, it } from "bun:test";
import type { Model } from "@gajae-code/ai";
import { buildNamedToolChoice } from "@gajae-code/coding-agent/utils/tool-choice";

describe("tool choice helpers", () => {
	it("builds a named Ollama choice for local forced tools", () => {
		const model = {
			id: "ggml-org/gemma-3-1b-it/GGUF",
			name: "Gemma 3 1B",
			api: "ollama-chat",
			provider: "ollama",
			baseUrl: "http://127.0.0.1:11434",
			reasoning: false,
			input: ["text"],
			cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
			contextWindow: 32_768,
			maxTokens: 8_192,
		} satisfies Model<"ollama-chat">;

		expect(buildNamedToolChoice("write", model)).toEqual({ type: "function", name: "write" });
	});
});
