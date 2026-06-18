export interface SkillDiscoverySettings {
	enabled?: boolean;
	enableSkillCommands?: boolean;
	enableCodexUser?: boolean;
	enableClaudeUser?: boolean;
	enableClaudeProject?: boolean;
	enablePiUser?: boolean;
	enablePiProject?: boolean;
	customDirectories?: string[];
	ignoredSkills?: string[];
	includeSkills?: string[];
}

export const DEFAULT_SKILL_DISCOVERY_SETTINGS: SkillDiscoverySettings = {
	enabled: false,
	enableSkillCommands: true,
	enableCodexUser: false,
	enableClaudeUser: false,
	enableClaudeProject: false,
	enablePiUser: false,
	enablePiProject: false,
	customDirectories: [],
	ignoredSkills: [],
	includeSkills: [],
};

export const DEFAULT_DISABLED_EXTENSIONS: string[] = [];
