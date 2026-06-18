import { beforeAll, describe, expect, test } from "bun:test";
import type { UsageLimit, UsageReport } from "@gajae-code/ai";
import { renderUsageReports } from "@gajae-code/coding-agent/modes/controllers/command-controller";
import { getThemeByName, setThemeInstance, theme } from "@gajae-code/coding-agent/modes/theme/theme";

function stripAnsi(text: string): string {
	return text.replace(/\x1b\[[0-9;]*m/g, "");
}

const NOW = 1_700_000_000_000;

function limit(windowId: string, label: string, windowLabel: string, resetMs: number, fraction: number): UsageLimit {
	return {
		label,
		status: "ok",
		amount: { usedFraction: fraction, unit: "percent" },
		scope: { provider: "anthropic", windowId },
		window: { id: windowId, label: windowLabel, resetsAt: NOW + resetMs },
	} as UsageLimit;
}

function report(email: string, fiveHour: number, sevenDay: number): UsageReport {
	return {
		provider: "anthropic",
		fetchedAt: NOW,
		metadata: { email },
		limits: [
			limit("5h", "Claude 5 Hour", "5 Hour", 2 * 3_600_000, fiveHour),
			limit("7d", "Claude 7 Day", "7 Day", 5 * 86_400_000, sevenDay),
		],
	} as UsageReport;
}

describe("usage report column ordering", () => {
	beforeAll(async () => {
		const loaded = await getThemeByName("red-claw");
		if (loaded) setThemeInstance(loaded);
	});

	test("accounts keep the same column across every window", () => {
		// alice has the higher TOTAL usage (0.2 + 0.6) but the lower 5h usage; bob
		// has the higher 5h usage. A per-window sort would put bob first in the 5h
		// row and alice first in the 7d row, so the columns would not line up.
		const reports = [report("alice@example.com", 0.2, 0.6), report("bob@example.com", 0.5, 0.1)];
		const lines = stripAnsi(renderUsageReports(reports, theme, NOW, 100)).split("\n");

		const headerAfter = (titleNeedle: string): string => {
			const titleIdx = lines.findIndex(line => line.includes(titleNeedle));
			expect(titleIdx).toBeGreaterThanOrEqual(0);
			return lines[titleIdx + 1] ?? "";
		};

		for (const header of [headerAfter("Claude 5 Hour"), headerAfter("Claude 7 Day")]) {
			const aliceCol = header.indexOf("alice@example.com");
			const bobCol = header.indexOf("bob@example.com");
			expect(aliceCol).toBeGreaterThanOrEqual(0);
			expect(bobCol).toBeGreaterThanOrEqual(0);
			// Same account order in every window row → columns line up vertically.
			expect(aliceCol).toBeLessThan(bobCol);
		}
	});
});
