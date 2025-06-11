'use client';

import React, { useState, useCallback, useEffect } from 'react';
import CodeEditor from '@/components/CodeEditor';
import { refactorCode, healthCheck, checkAuthStatus } from '@/services/api';
import { LanguageOption, AppState } from '@/types';

const LANGUAGES: LanguageOption[] = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
  { value: 'csharp', label: 'C#' },
  { value: 'go', label: 'Go' },
  { value: 'rust', label: 'Rust' },
  { value: 'php', label: 'PHP' },
  { value: 'ruby', label: 'Ruby' },
  { value: 'swift', label: 'Swift' },
  { value: 'kotlin', label: 'Kotlin' },
  { value: 'scala', label: 'Scala' },
  { value: 'r', label: 'R' },
  { value: 'sql', label: 'SQL' },
  { value: 'html', label: 'HTML' },
  { value: 'css', label: 'CSS' }
];

const SAMPLE_CODE = `def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def main():
    number = 5
    result = calculate_factorial(number)
    print(f"Factorial of {number} is {result}")

if __name__ == "__main__":
    main()`;

export default function HomePage() {
  const [state, setState] = useState<AppState>({
    inputCode: SAMPLE_CODE,
    outputCode: '',
    language: 'python',
    focus: 'readability',
    isLoading: false,
    error: null
  });

  const [backendStatus, setBackendStatus] = useState<string>('checking');
  const [authStatus, setAuthStatus] = useState<string>('checking');
  const [authMessage, setAuthMessage] = useState<string>('');

  // Check backend connection and authentication status
  useEffect(() => {
    const checkBackendAndAuth = async () => {
      try {
        // Check backend health
        await healthCheck();
        setBackendStatus('connected');
        console.log('✅ Backend connection established');
        
        // Check authentication
        try {
          const authResult = await checkAuthStatus();
          if (authResult.authenticated) {
            setAuthStatus('authenticated');
            setAuthMessage('Authentication successful');
            console.log('✅ Authentication successful');
          } else {
            setAuthStatus('unauthenticated');
            setAuthMessage(authResult.message || 'Authentication required');
            console.log('🔓 No authentication required or auth disabled');
          }
        } catch (authError) {
          setAuthStatus('failed');
          setAuthMessage('Authentication failed - please check your API token');
          console.error('❌ Authentication failed:', authError);
        }
        
      } catch (error) {
        setBackendStatus('disconnected');
        setAuthStatus('unknown');
        console.error('❌ Backend connection failed:', error);
        setState(prev => ({ 
          ...prev, 
          error: 'Cannot connect to backend service. Please ensure the backend is running on http://localhost:8000' 
        }));
      }
    };

    checkBackendAndAuth();
  }, []);

  const handleInputChange = useCallback((value: string) => {
    setState(prev => ({ ...prev, inputCode: value, error: null }));
  }, []);

  const handleLanguageChange = useCallback((language: string) => {
    setState(prev => ({ ...prev, language, error: null }));
  }, []);

  const handleRefactor = useCallback(async () => {
    if (!state.inputCode.trim()) {
      setState(prev => ({ ...prev, error: 'Please enter some code to refactor.' }));
      return;
    }

    if (backendStatus !== 'connected') {
      setState(prev => ({ ...prev, error: 'Backend service is not available. Please check the connection.' }));
      return;
    }

    if (authStatus === 'failed') {
      setState(prev => ({ ...prev, error: 'Authentication failed. Please check your API token configuration.' }));
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const result = await refactorCode({
        code: state.inputCode,
        language: state.language
      });

      if (result.success) {
        setState(prev => ({
          ...prev,
          outputCode: result.refactored_code,
          isLoading: false
        }));
      } else {
        setState(prev => ({
          ...prev,
          error: result.error || 'Refactoring failed',
          isLoading: false
        }));
      }
    } catch (error) {
      console.error('Refactor error:', error);
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'An unexpected error occurred',
        isLoading: false
      }));
    }
  }, [state.inputCode, state.language, backendStatus, authStatus]);

  const isRefactorDisabled = state.isLoading || !state.inputCode.trim() || backendStatus !== 'connected' || authStatus === 'failed';

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'Arial, sans-serif' }}>
      {/* Simple top bar */}
      <div style={{ 
        padding: '10px', 
        borderBottom: '1px solid #ccc', 
        backgroundColor: '#f5f5f5',
        display: 'flex',
        alignItems: 'center',
        gap: '15px'
      }}>
        <h1 style={{ margin: 0, fontSize: '20px' }}>Code Refinery</h1>
        
        {/* Backend status indicator */}
        <div style={{
          fontSize: '12px',
          padding: '2px 8px',
          borderRadius: '4px',
          backgroundColor: backendStatus === 'connected' ? '#d4edda' : backendStatus === 'disconnected' ? '#f8d7da' : '#fff3cd',
          color: backendStatus === 'connected' ? '#155724' : backendStatus === 'disconnected' ? '#721c24' : '#856404',
          border: `1px solid ${backendStatus === 'connected' ? '#c3e6cb' : backendStatus === 'disconnected' ? '#f5c6cb' : '#ffeaa7'}`
        }}>
          Backend: {backendStatus === 'connected' ? '✅ Connected' : backendStatus === 'disconnected' ? '❌ Disconnected' : '🔄 Checking...'}
        </div>

        {/* Authentication status indicator */}
        <div style={{
          fontSize: '12px',
          padding: '2px 8px',
          borderRadius: '4px',
          backgroundColor: authStatus === 'authenticated' ? '#d4edda' : authStatus === 'failed' ? '#f8d7da' : authStatus === 'unauthenticated' ? '#fff3cd' : '#e2e3e5',
          color: authStatus === 'authenticated' ? '#155724' : authStatus === 'failed' ? '#721c24' : authStatus === 'unauthenticated' ? '#856404' : '#6c757d',
          border: `1px solid ${authStatus === 'authenticated' ? '#c3e6cb' : authStatus === 'failed' ? '#f5c6cb' : authStatus === 'unauthenticated' ? '#ffeaa7' : '#d6d8db'}`
        }}>
          Auth: {authStatus === 'authenticated' ? '🔐 Authenticated' : 
                 authStatus === 'failed' ? '❌ Failed' :
                 authStatus === 'unauthenticated' ? '🔓 Not Required' :
                 '🔄 Checking...'}
        </div>
        
        <select
          value={state.language}
          onChange={(e) => handleLanguageChange(e.target.value)}
          style={{
            padding: '5px 10px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.value} value={lang.value}>
              {lang.label}
            </option>
          ))}
        </select>

        <button
          onClick={handleRefactor}
          disabled={isRefactorDisabled}
          style={{
            padding: '8px 16px',
            backgroundColor: isRefactorDisabled ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isRefactorDisabled ? 'not-allowed' : 'pointer'
          }}
        >
          {state.isLoading ? 'Refactoring...' : 'Refactor Code'}
        </button>

        {state.error && (
          <div style={{ color: 'red', fontSize: '14px', maxWidth: '300px' }}>
            {state.error}
          </div>
        )}

        {authMessage && authStatus !== 'checking' && (
          <div style={{ 
            fontSize: '12px', 
            color: authStatus === 'failed' ? '#721c24' : '#6c757d',
            maxWidth: '200px'
          }}>
            {authMessage}
          </div>
        )}
      </div>

      {/* Main editor area */}
      <div style={{ 
        flex: 1, 
        display: 'flex',
        gap: '1px',
        backgroundColor: '#ccc'
      }}>
        {/* Left: Input Editor */}
        <div style={{ 
          flex: 1,
          backgroundColor: 'white',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <div style={{
            padding: '8px 12px',
            backgroundColor: '#f8f9fa',
            borderBottom: '1px solid #dee2e6',
            fontSize: '14px',
            fontWeight: 'bold'
          }}>
            Input Code
          </div>
          <div style={{ flex: 1 }}>
            <CodeEditor
              value={state.inputCode}
              onChange={handleInputChange}
              language={state.language}
              placeholder="Enter your code here..."
            />
          </div>
        </div>

        {/* Right: Output Editor */}
        <div style={{ 
          flex: 1,
          backgroundColor: 'white',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <div style={{
            padding: '8px 12px',
            backgroundColor: '#f8f9fa',
            borderBottom: '1px solid #dee2e6',
            fontSize: '14px',
            fontWeight: 'bold'
          }}>
            Refactored Code
          </div>
          <div style={{ flex: 1 }}>
            <CodeEditor
              value={state.outputCode}
              onChange={() => {}} // Read-only
              language={state.language}
              readOnly={true}
              placeholder="Refactored code will appear here..."
            />
          </div>
        </div>
      </div>
    </div>
  );
}
