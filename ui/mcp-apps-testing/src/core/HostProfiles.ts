/**
 * Host Profiles - Simulates different MCP host environments
 * 
 * This module provides pre-configured profiles for different AI host environments
 * like Claude, VS Code, etc., including their specific capabilities, theme variables,
 * and constraints.
 */

export interface HostProfile {
  name: string;
  capabilities: {
    tools?: { listChanged?: boolean };
    resources?: { subscribe?: boolean; listChanged?: boolean };
    prompts?: { listChanged?: boolean };
  };
  theme: {
    light: Record<string, string>;
    dark: Record<string, string>;
  };
  constraints?: {
    maxViewportWidth?: number;
    maxViewportHeight?: number;
    allowedProtocols?: string[];
  };
}

/**
 * Claude AI host profile
 */
export const ClaudeProfile: HostProfile = {
  name: 'Claude',
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: true, listChanged: true },
    prompts: { listChanged: true },
  },
  theme: {
    light: {
      '--background': '#ffffff',
      '--foreground': '#1a1a1a',
      '--primary': '#6366f1',
      '--secondary': '#8b5cf6',
      '--accent': '#ec4899',
      '--muted': '#f3f4f6',
      '--border': '#e5e7eb',
    },
    dark: {
      '--background': '#1a1a1a',
      '--foreground': '#ffffff',
      '--primary': '#818cf8',
      '--secondary': '#a78bfa',
      '--accent': '#f472b6',
      '--muted': '#374151',
      '--border': '#4b5563',
    },
  },
  constraints: {
    maxViewportWidth: 1920,
    maxViewportHeight: 1080,
    allowedProtocols: ['http', 'https', 'data'],
  },
};

/**
 * VS Code host profile
 */
export const VSCodeProfile: HostProfile = {
  name: 'VS Code',
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: false, listChanged: true },
    prompts: { listChanged: false },
  },
  theme: {
    light: {
      '--background': '#ffffff',
      '--foreground': '#333333',
      '--primary': '#007acc',
      '--secondary': '#68217a',
      '--accent': '#0098ff',
      '--muted': '#f3f3f3',
      '--border': '#cccccc',
    },
    dark: {
      '--background': '#1e1e1e',
      '--foreground': '#cccccc',
      '--primary': '#0098ff',
      '--secondary': '#c586c0',
      '--accent': '#4fc1ff',
      '--muted': '#2d2d2d',
      '--border': '#3e3e3e',
    },
  },
  constraints: {
    maxViewportWidth: 1600,
    maxViewportHeight: 900,
    allowedProtocols: ['http', 'https', 'vscode', 'data'],
  },
};

/**
 * Generic host profile (default)
 */
export const GenericProfile: HostProfile = {
  name: 'Generic',
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: true, listChanged: true },
    prompts: { listChanged: true },
  },
  theme: {
    light: {
      '--background': '#ffffff',
      '--foreground': '#000000',
      '--primary': '#0066cc',
      '--secondary': '#6600cc',
      '--accent': '#cc0066',
      '--muted': '#f5f5f5',
      '--border': '#dddddd',
    },
    dark: {
      '--background': '#000000',
      '--foreground': '#ffffff',
      '--primary': '#3399ff',
      '--secondary': '#9933ff',
      '--accent': '#ff3399',
      '--muted': '#333333',
      '--border': '#555555',
    },
  },
};

/**
 * Available host profiles
 */
export const HostProfiles = {
  Claude: ClaudeProfile,
  VSCode: VSCodeProfile,
  Generic: GenericProfile,
} as const;

/**
 * Apply theme CSS variables to a page or element
 */
export function applyTheme(
  profile: HostProfile,
  mode: 'light' | 'dark' = 'light'
): string {
  const themeVars = profile.theme[mode];
  return Object.entries(themeVars)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n');
}
