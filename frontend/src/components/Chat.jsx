import React, { useState, useRef } from 'react';
import axios from 'axios';
import './Chat.css';

const BACKEND_URL = 'https://bhsvirtualhealthassistant.onrender.com';

function formatAssistantResponse(text) {
  if (!text) return null;
  const lines = text.split(/\r?\n/).map(l => l.trim());
  const elements = [];
  let bullets = [];
  let inBullets = false;

  // Heading: first non-empty line
  let i = 0;
  while (i < lines.length && !lines[i]) i++;
  if (i < lines.length) {
    elements.push(<strong key="heading">{lines[i]}</strong>);
    i++;
  }

  for (; i < lines.length; i++) {
    const line = lines[i];
    if (!line) continue;
    if (line.startsWith('•') || line.startsWith('-')) {
      bullets.push(line.replace(/^[-•]\s*/, ''));
      inBullets = true;
    } else {
      if (inBullets && bullets.length) {
        elements.push(
          <ul key={elements.length + '-ul'}>
            {bullets.map((b, j) => <li key={j}>{b}</li>)}
          </ul>
        );
        bullets = [];
        inBullets = false;
      }
      // Sources or disclaimer
      if (/^Sources?:/i.test(line) || /For emergencies call 119/i.test(line)) {
        elements.push(<div key={elements.length + '-src'} style={{ fontSize: '0.9em', fontStyle: 'italic', marginTop: 8 }}>{line}</div>);
      } else {
        elements.push(<p key={elements.length + '-p'}>{line}</p>);
      }
    }
  }
  if (bullets.length) {
    elements.push(
      <ul key={elements.length + '-ul-end'}>
        {bullets.map((b, j) => <li key={j}>{b}</li>)}
      </ul>
    );
  }
  return elements;
}

export default function Chat({ language }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showNurse, setShowNurse] = useState(false);
  const chatRef = useRef(null);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/chat`, {
        messages: updatedMessages,
        consent: true,
        chat_id: 'demo',
      });
      setMessages(msgs => [...updatedMessages, { role: 'assistant', content: res.data.answer }]);
      setShowNurse(true);
    } catch (err) {
      setMessages(msgs => [...updatedMessages, { role: 'assistant', content: 'Sorry, there was an error.' }]);
    }
    setLoading(false);
    setTimeout(() => {
      if (chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }, 100);
  };

  const handleNurseCallback = () => {
    alert('A nurse will contact you within 30 minutes.');
    // TODO: Implement nurse call-back logic
  };

  return (
    <div className="chat-container">
      <div className="chat-messages" ref={chatRef}>
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.role}`}>{
            msg.role === 'assistant' ? formatAssistantResponse(msg.content) : msg.content
          }</div>
        ))}
        {loading && <div className="msg assistant">Typing...</div>}
      </div>
      <form className="chat-input" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={language === 'patwa' ? 'Type yuh message...' : 'Type your message...'}
          aria-label="Message"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
      </form>
      {showNurse && (
        <button className="nurse-btn" onClick={handleNurseCallback}>
          Request Nurse Call-Back
        </button>
      )}
    </div>
  );
} 