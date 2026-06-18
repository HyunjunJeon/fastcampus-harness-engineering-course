import { describe, expect, it } from "bun:test";
import { BUILTIN_MODEL_PROFILES } from "../src/config/model-profiles";
import { getBundledGrokBuildExtensionFactory, getBundledGrokCliModelDefaults } from "../src/defaults/gjc-grok-cli";

describe("Grok Build post-merge sequence", () => {
	it("ships the extension, reference models, and grok-build-pro profile needed by the user flow", () => {
		expect(typeof getBundledGrokBuildExtensionFactory()).toBe("function");
		expect(getBundledGrokCliModelDefaults()).toContain("grok-composer-2.5-fast");

		const profile = BUILTIN_MODEL_PROFILES.find(definition => definition.name === "grok-build-pro");
		expect(profile?.requiredProviders).toContain("grok-build");
		expect(profile?.modelMapping.default).toBe("grok-build/grok-composer-2.5-fast");
		expect(profile?.modelMapping.executor).toBe("grok-build/grok-build");
	});
});
