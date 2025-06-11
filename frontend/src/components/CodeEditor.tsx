'use client';

import React from 'react';
import { Editor } from '@monaco-editor/react';
import { CodeEditorProps } from '@/types';

const CodeEditor: React.FC<CodeEditorProps> = ({ 
  value, 
  onChange, 
  language, 
  readOnly = false, 
  placeholder = "Enter your code here..." 
}) => {
  const getMonacoLanguage = (lang: string): string => {
    const languageMap: Record<string, string> = {
      'cpp': 'cpp',
      'c': 'c',
      'csharp': 'csharp',
      'python': 'python',
      'javascript': 'javascript',
      'typescript': 'typescript',
      'java': 'java',
      'go': 'go',
      'rust': 'rust',
      'php': 'php',
      'ruby': 'ruby',
      'swift': 'swift',
      'kotlin': 'kotlin',
      'scala': 'scala',
      'r': 'r',
      'sql': 'sql',
      'html': 'html',
      'css': 'css'
    };
    
    return languageMap[lang.toLowerCase()] || 'plaintext';
  };

  const editorOptions = {
    selectOnLineNumbers: true,
    readOnly: readOnly,
    automaticLayout: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    wordWrap: 'on' as const,
    wrappingStrategy: 'advanced' as const,
    fontSize: 14,
    lineHeight: 20,
    formatOnPaste: true,
    formatOnType: true,
    autoIndent: 'full' as const,
    scrollbar: {
      verticalScrollbarSize: 10,
      horizontalScrollbarSize: 10
    }
  };

  const handleEditorDidMount = (editor: unknown, monaco: unknown) => {
    // Type assertion for monaco API
    const monacoApi = monaco as { editor: { setTheme: (theme: string) => void } };
    const editorInstance = editor as { focus: () => void };
    
    monacoApi.editor.setTheme('vs');
    
    if (!readOnly && !value) {
      setTimeout(() => {
        editorInstance.focus();
      }, 100);
    }
  };

  const handleChange = (newValue: string | undefined) => {
    if (onChange && !readOnly) {
      onChange(newValue || '');
    }
  };

  const displayValue = value || (readOnly ? '' : placeholder);

  return (
    <Editor
      height="100%"
      width="100%"
      language={getMonacoLanguage(language)}
      value={displayValue}
      onChange={handleChange}
      onMount={handleEditorDidMount}
      options={editorOptions}
      loading={<div style={{ padding: '20px', textAlign: 'center' }}>Loading editor...</div>}
    />
  );
};

export default CodeEditor;