/**
 * Regression guard for Korean IME cursor positioning in the Input component.
 *
 * Compatibility jamo (U+3131..U+318E) are terminal-wide glyphs, so the cursor
 * column should advance by two cells per typed jamo. Conjoining jamo input is
 * normalized to NFC elsewhere; this test covers the compatibility-jamo path.
 */
import { describe, expect, it } from "bun:test";
import { CURSOR_MARKER } from "@gajae-code/tui";
import { Input } from "@gajae-code/tui/components/input";
import { visibleWidth } from "@gajae-code/tui/utils";

/**
 * Drive `text` through `Input.handleInput()` one Unicode code point at a
 * time (mirrors what the IME does — one code point per emitted sequence),
 * then return the visual column where the hardware cursor marker lands
 * in the rendered output.
 */
function cursorColAfterTyping(text: string, width = 80): number {
	const input = new Input();
	(input as unknown as { focused: boolean }).focused = true;
	for (const char of text) {
		input.handleInput(char);
	}
	const [line] = input.render(width);
	const markerIdx = line.indexOf(CURSOR_MARKER);
	if (markerIdx < 0) {
		throw new Error(`CURSOR_MARKER not found in rendered line: ${JSON.stringify(line)}`);
	}
	return visibleWidth(line.slice(0, markerIdx));
}

const PROMPT_WIDTH = 2; // "> "

describe("Input cursor column tracks compatibility jamo width", () => {
	it("ASCII baseline: cursor lands exactly after the typed text", () => {
		expect(cursorColAfterTyping("hello")).toBe(PROMPT_WIDTH + 5);
	});

	it("Hangul syllables: cursor lands exactly after typed text (2 cells each)", () => {
		expect(cursorColAfterTyping("안녕")).toBe(PROMPT_WIDTH + 4);
	});

	it("single compatibility jamo advances by 2 cells", () => {
		expect(cursorColAfterTyping("ㅁ")).toBe(PROMPT_WIDTH + 2);
	});

	it("8 consecutive compatibility jamo advance by 16 cells", () => {
		expect(cursorColAfterTyping("ㅁㄴㅁㄴㅇㅂㄴㅂ")).toBe(PROMPT_WIDTH + 16);
	});

	it("20 consecutive compatibility jamo advance by 40 cells", () => {
		const jamo = "ㅁㄴㄷㅂㅈㅎㅋㅌㄱㄹ".repeat(2);
		expect(cursorColAfterTyping(jamo, 120)).toBe(PROMPT_WIDTH + 40);
	});

	it("cursor column grows by 2 per typed compatibility jamo", () => {
		const input = new Input();
		(input as unknown as { focused: boolean }).focused = true;
		const jamo = "ㅁㄴㅇㅂㅈㅎㅋㅌㄷㄹ";
		let prevCol = PROMPT_WIDTH;
		for (let i = 0; i < jamo.length; i++) {
			input.handleInput(jamo[i]);
			const [line] = input.render(80);
			const markerIdx = line.indexOf(CURSOR_MARKER);
			const col = visibleWidth(line.slice(0, markerIdx));
			const delta = col - prevCol;
			expect(delta).toBe(2);
			prevCol = col;
		}
	});
});
