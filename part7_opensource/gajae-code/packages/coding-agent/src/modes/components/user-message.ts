import { type Component, Container, Markdown, Spacer, Text } from "@gajae-code/tui";
import { getMarkdownTheme, theme } from "../../modes/theme/theme";

// OSC 133 shell integration: marks prompt zones for terminal multiplexers
const OSC133_ZONE_START = "\x1b]133;A\x07";
const OSC133_ZONE_END = "\x1b]133;B\x07";
const OSC133_ZONE_FINAL = "\x1b]133;C\x07";

/**
 * Component that renders a user message
 */
export class UserMessageComponent extends Container {
	constructor(text: string, synthetic = false) {
		super();
		const bgColor = (value: string) => theme.bg("userMessageBg", value);
		const color = synthetic
			? (value: string) => theme.fg("dim", value)
			: (value: string) => theme.fg("userMessageText", value);
		this.addChild(new Spacer(1));
		const label = synthetic ? "replay" : "user";
		this.addChild(new Text(theme.bold(theme.fg("accent", label)), 1, 0));
		this.addChild(new PromptZoneMarkdown(text, bgColor, color));
	}
}

class PromptZoneMarkdown implements Component {
	#markdown: Markdown;

	constructor(text: string, bgColor: (value: string) => string, color: (value: string) => string) {
		this.#markdown = new Markdown(text, 1, 1, getMarkdownTheme(), {
			bgColor,
			color,
		});
	}

	invalidate(): void {
		this.#markdown.invalidate();
	}

	render(width: number): string[] {
		const lines = this.#markdown.render(width);
		if (lines.length === 0) {
			return lines;
		}

		const zoned = [...lines];
		zoned[0] = OSC133_ZONE_START + zoned[0];
		zoned[zoned.length - 1] = `${zoned[zoned.length - 1]}${OSC133_ZONE_END}${OSC133_ZONE_FINAL}`;
		return zoned;
	}
}
