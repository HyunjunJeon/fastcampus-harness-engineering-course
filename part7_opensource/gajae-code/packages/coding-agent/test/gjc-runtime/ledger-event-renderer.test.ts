import { describe, expect, it } from "bun:test";
import {
	coerceUltragoalLedgerEvent,
	formatRalplanStagePresence,
	latestUltragoalLedgerEvent,
	latestUltragoalLedgerEventFromText,
	parseRalplanIndexLine,
	parseUltragoalLedgerLine,
	type RalplanIndexRow,
	summarizeRalplanIndex,
} from "../../src/gjc-runtime/ledger-event-renderer";

describe("ledger-event-renderer: ultragoal", () => {
	it("parses the event-keyed vocabulary", () => {
		expect(parseUltragoalLedgerLine('{"event":"goal_checkpointed","goalId":"G003","status":"complete"}')).toEqual({
			event: "goal_checkpointed",
			goalId: "G003",
			status: "complete",
		});
	});

	it("parses the type-keyed reconcile_failed row", () => {
		expect(parseUltragoalLedgerLine('{"type":"reconcile_failed","error":"boom"}')).toEqual({
			event: "reconcile_failed",
		});
	});

	it("skips blank and malformed lines", () => {
		expect(parseUltragoalLedgerLine("")).toBeUndefined();
		expect(parseUltragoalLedgerLine("   ")).toBeUndefined();
		expect(parseUltragoalLedgerLine("{not json")).toBeUndefined();
		expect(parseUltragoalLedgerLine("[1,2,3]")).toBeUndefined();
		expect(parseUltragoalLedgerLine('{"goalId":"G001"}')).toBeUndefined();
	});

	it("coerces already-parsed rows", () => {
		expect(coerceUltragoalLedgerEvent({ event: "goal_started", goalId: "G001" })).toEqual({
			event: "goal_started",
			goalId: "G001",
		});
		expect(coerceUltragoalLedgerEvent({ nothing: true })).toBeUndefined();
	});

	it("returns the latest event, or undefined for an empty ledger", () => {
		expect(latestUltragoalLedgerEvent([])).toBeUndefined();
		const events = [
			{ event: "plan_created" },
			{ event: "goal_started", goalId: "G001" },
			{ event: "goal_checkpointed", goalId: "G001", status: "complete" },
		];
		expect(latestUltragoalLedgerEvent(events)).toEqual({
			event: "goal_checkpointed",
			goalId: "G001",
			status: "complete",
		});
	});

	it("reads the latest event from raw text, skipping malformed/blank lines", () => {
		const text = [
			'{"event":"plan_created"}',
			"{not json",
			"",
			'{"event":"goal_started","goalId":"G001"}',
			'{"type":"reconcile_failed","error":"boom"}',
		].join("\n");
		expect(latestUltragoalLedgerEventFromText(text)).toEqual({ event: "reconcile_failed" });
		expect(latestUltragoalLedgerEventFromText("")).toBeUndefined();
		expect(latestUltragoalLedgerEventFromText("{bad\n  \n")).toBeUndefined();
	});
});

describe("ledger-event-renderer: ralplan", () => {
	it("parses index rows and skips malformed lines", () => {
		expect(parseRalplanIndexLine('{"stage":"planner","stage_n":1,"path":"p","sha256":"h"}')).toEqual({
			stage: "planner",
			stageN: 1,
		});
		expect(parseRalplanIndexLine("")).toBeUndefined();
		expect(parseRalplanIndexLine("{bad")).toBeUndefined();
		expect(parseRalplanIndexLine('{"stage_n":1}')).toBeUndefined();
	});

	it("treats planner=1 + architect=2 in the same run as ONE iteration", () => {
		const rows: RalplanIndexRow[] = [
			{ stage: "planner", stageN: 1 },
			{ stage: "architect", stageN: 2 },
		];
		expect(summarizeRalplanIndex(rows)).toEqual({ iteration: 1, currentStages: ["planner", "architect"] });
	});

	it("opens a new iteration on revision and tracks the current iteration's stages", () => {
		const rows: RalplanIndexRow[] = [
			{ stage: "planner", stageN: 1 },
			{ stage: "architect", stageN: 1 },
			{ stage: "critic", stageN: 1 },
			{ stage: "revision", stageN: 2 },
			{ stage: "architect", stageN: 2 },
		];
		expect(summarizeRalplanIndex(rows)).toEqual({ iteration: 2, currentStages: ["revision", "architect"] });
	});

	it("counts rows before any opener as one iteration", () => {
		expect(summarizeRalplanIndex([{ stage: "architect" }])).toEqual({
			iteration: 1,
			currentStages: ["architect"],
		});
		expect(summarizeRalplanIndex([])).toEqual({ iteration: 0, currentStages: [] });
	});

	it("formats a compact stage-presence string and collapses past the cap", () => {
		expect(formatRalplanStagePresence([])).toBeUndefined();
		expect(formatRalplanStagePresence(["planner", "architect", "critic"])).toBe("P·A·C");
		const collapsed = formatRalplanStagePresence(["planner", "architect", "critic", "revision"], 2);
		expect(collapsed).toBe("P·A … 2 more stages");
	});
});
