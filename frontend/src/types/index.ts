// API request and response type definitions
export interface RefactorRequest {
  code: string;
  language: string;
}

export interface RefactorResponse {
  refactored_code: string;
  language: string;
  success: boolean;
  error?: string;
}

// UI component types
export interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  readOnly?: boolean;
  placeholder?: string;
}

// Application state types
export interface AppState {
  inputCode: string;
  outputCode: string;
  language: string;
  focus: string;
  isLoading: boolean;
  error: string | null;
}

// Language option types
export interface LanguageOption {
  value: string;
  label: string;
}

// Refactor focus option types
export interface FocusOption {
  value: string;
  label: string;
  description: string;
} 