import { describe, expect, it } from "bun:test";
import vendorPackage from "../src/defaults/gjc/extensions/grok-cli-vendor/package.json";

describe("bundled Grok CLI vendor dependencies", () => {
	it("does not require runtime npm install from setup defaults", async () => {
		const pkg = vendorPackage as { dependencies?: Record<string, string> };
		expect(pkg.dependencies ?? {}).toEqual({});
	});
});
