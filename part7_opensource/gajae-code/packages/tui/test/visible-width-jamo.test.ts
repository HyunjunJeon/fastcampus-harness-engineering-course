/**
 * Regression guard for Hangul terminal width handling.
 *
 * Hangul Compatibility Jamo (U+3131..U+318E, e.g. `ㅁ`) are East Asian Wide
 * and xterm-compatible terminals render them as 2 cells. Undercounting them
 * lets the TUI write lines it believes fit while the terminal auto-wraps the
 * row, producing the diagonal/pyramid Korean rendering failure.
 *
 * Conjoining jamo sequences (U+1100..U+11FF, e.g. `한`) are different:
 * terminals render each grapheme cluster like its NFC syllable, so width
 * measurement must normalize those sequences before calling Bun.stringWidth.
 */
import { describe, expect, it } from "bun:test";
import { Ellipsis, sliceWithWidth, truncateToWidth, visibleWidth } from "@gajae-code/tui/utils";

describe("visibleWidth — Hangul width parity", () => {
	it("single compatibility jamo is 2 cells", () => {
		// U+3141 HANGUL LETTER MIEUM
		expect(visibleWidth("ㅁ")).toBe(2);
		// U+3134 HANGUL LETTER NIEUN
		expect(visibleWidth("ㄴ")).toBe(2);
		// U+3147 HANGUL LETTER IEUNG
		expect(visibleWidth("ㅇ")).toBe(2);
		// U+3142 HANGUL LETTER PIEUP
		expect(visibleWidth("ㅂ")).toBe(2);
		// U+3148 HANGUL LETTER JIEUJ
		expect(visibleWidth("ㅈ")).toBe(2);
	});

	it("range edges U+3131 and U+318E are wide", () => {
		// U+3131 HANGUL LETTER KIYEOK — first jamo in the block
		expect(visibleWidth("\u3131")).toBe(2);
		// U+318E HANGUL LETTER ARAEAE — last jamo in the block
		expect(visibleWidth("\u318e")).toBe(2);
	});

	it("U+3164 HANGUL FILLER is 2 cells", () => {
		expect(visibleWidth("\u3164")).toBe(2);
	});

	it("string of 8 consecutive compatibility jamo is 16 cells", () => {
		expect(visibleWidth("ㅁㄴㅁㄴㅇㅂㄴㅂ")).toBe(16);
	});

	it("Hangul Syllables (U+AC00..U+D7A3) stay at 2 cells", () => {
		// `안` U+C548 — composed syllable, must remain 2 cells
		expect(visibleWidth("안")).toBe(2);
		// `녕` U+B155 — composed syllable
		expect(visibleWidth("녕")).toBe(2);
		// Whole word: 안녕 = 4 cells
		expect(visibleWidth("안녕")).toBe(4);
		// First & last in the block, for boundary coverage
		expect(visibleWidth("\uac00")).toBe(2); // 가
		expect(visibleWidth("\ud7a3")).toBe(2); // 힣
	});

	it("conjoining jamo sequences use NFC terminal width", () => {
		// Some macOS input paths deliver Hangul syllables as conjoining jamo
		// (NFD). Terminals render them as the composed syllable, so width must
		// match NFC or the hardware cursor drifts one cell per syllable.
		expect(visibleWidth("하")).toBe(2);
		expect(visibleWidth("한")).toBe(2);
		expect(visibleWidth("한글")).toBe(4);
	});

	it("mixed ASCII + syllable + jamo strings add correctly", () => {
		// a (1) + 안 (2) + ㅂ (2) + b (1) = 6
		expect(visibleWidth("a안ㅂb")).toBe(6);
		// 11 ASCII letters + 1 syllable + 4 jamo = 11 + 2 + 8 = 21
		expect(visibleWidth("hello world안ㅁㄴㅇㅂ")).toBe(11 + 2 + 8);
	});

	it("does not regress ASCII fast path or empty input", () => {
		expect(visibleWidth("")).toBe(0);
		expect(visibleWidth("hello")).toBe(5);
		expect(visibleWidth("a")).toBe(1);
		// Tab character (ASCII 0x09) inside the fast path expands to >2
		expect(visibleWidth("a\tb")).toBeGreaterThan(2);
	});

	it("does not change width for other CJK characters", () => {
		// Chinese: 漢字 (each 2 cells)
		expect(visibleWidth("漢字")).toBe(4);
		// Japanese hiragana: あい (each 2 cells)
		expect(visibleWidth("あい")).toBe(4);
		// Japanese katakana: アイ (each 2 cells)
		expect(visibleWidth("アイ")).toBe(4);
	});

	it("Halfwidth Hangul block is unaffected (already Narrow in Bun)", () => {
		// U+FFA1 HALFWIDTH HANGUL LETTER KIYEOK — Bun reports 1, untouched.
		expect(visibleWidth("\uffa1")).toBe(1);
		// U+FFDC HALFWIDTH HANGUL LETTER I
		expect(visibleWidth("\uffdc")).toBe(1);
	});
});

describe("native text helpers — Hangul Compatibility Jamo width parity", () => {
	it("sliceWithWidth treats jamo as 2 cells per character", () => {
		const input = "ㅁ".repeat(8);
		const { text, width } = sliceWithWidth(input, 0, 8, true);
		expect(text).toBe("ㅁ".repeat(4));
		expect(width).toBe(8);
	});

	it("truncateToWidth keeps 4 jamo within an 8-cell budget", () => {
		const result = truncateToWidth("ㅁ".repeat(20), 8, Ellipsis.Omit);
		const jamo = result.replaceAll(/[^\u3131-\u318E]/g, "");
		expect(jamo.length).toBe(4);
	});

	it("native and TS visibleWidth agree on a jamo run", () => {
		const input = "ㅁㄴㅇㅂㅈㄷㄱㅅ";
		expect(visibleWidth(input)).toBe(16);
		expect(sliceWithWidth(input, 0, 8, true).width).toBe(8);
	});
});
