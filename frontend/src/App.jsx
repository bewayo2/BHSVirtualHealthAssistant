import React, { useState } from 'react';
import Chat from './components/Chat';
import './App.css';

export default function App() {
  const [contrast, setContrast] = useState(false);
  const [fontSize, setFontSize] = useState(1);
  const [language, setLanguage] = useState('en');

  return (
    <div className={contrast ? 'app high-contrast' : 'app'} style={{ fontSize: `${fontSize}em` }}>
      <header>
        <h1>BHS Virtual Health Assistant</h1>
        <div className="toolbar">
          <button onClick={() => setContrast(c => !c)}>{contrast ? 'Normal' : 'High Contrast'}</button>
          <button onClick={() => setFontSize(f => Math.max(0.8, f - 0.1))}>A-</button>
          <button onClick={() => setFontSize(f => Math.min(2, f + 0.1))}>A+</button>
          <button onClick={() => setLanguage(l => l === 'en' ? 'patwa' : 'en')}>
            {language === 'en' ? 'Patwa' : 'English'}
          </button>
        </div>
      </header>
      <main>
        <Chat language={language} />
      </main>
      <footer>
        <small>All chats are private and secure. For emergencies call 119.</small>
      </footer>
    </div>
  );
} 