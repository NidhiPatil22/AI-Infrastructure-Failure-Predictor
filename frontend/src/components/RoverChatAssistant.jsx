import React, { useState, useEffect, useRef } from 'react';
import { sendChatMessage, getChatStatus, getApiErrorMessage } from '../services/api.js';

const SUGGESTED_PROMPTS = [
  'What can this project do?',
  'How does failure prediction work?',
  'Explain road damage detection',
  'What is the predicted remaining useful life?',
  'How does maintenance optimization work?',
  'Help me navigate the dashboard',
];

const INITIAL_WELCOME = {
  role: 'assistant',
  content:
    '👋 **Hello Engineer! I am ROVER — Road Operations & Vulnerability Evaluation Robot.**\n\n' +
    'I am your intelligent assistant for this predictive maintenance platform. Ask me anything about:\n' +
    '• **Structural Failure Risk:** How ML classifiers forecast infrastructure hazards\n' +
    '• **Pavement Distress (CV):** How OpenCV & YOLO inspect cracks, potholes, and compute the RDI\n' +
    '• **Prognostic RUL:** How regression models estimate operational lifespan in years\n' +
    '• **Knapsack Optimization:** How combinatorial algorithms prioritize maintenance allocations\n\n' +
    '*Click a suggested question or type below to begin!*',
};

export default function RoverChatAssistant() {
  const [messages, setMessages] = useState([INITIAL_WELCOME]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ configured: false, provider: 'gemini', model: 'gemini-2.0-flash' });
  const messagesEndRef = useRef(null);

  useEffect(() => {
    getChatStatus()
      .then((data) => setStatus(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const prompt = (textToSend || input).trim();
    if (!prompt || loading) return;

    const userMsg = { role: 'user', content: prompt };
    const nextHistory = [...messages, userMsg];
    setMessages(nextHistory);
    setInput('');
    setLoading(true);

    try {
      const historyPayload = nextHistory
        .slice(-8)
        .map((m) => ({ role: m.role, content: m.content }));
      const response = await sendChatMessage(prompt, historyPayload);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.response || 'No response returned.' },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `⚠️ **ROVER Notice:** ${getApiErrorMessage(err)}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleReset = () => {
    setMessages([INITIAL_WELCOME]);
  };

  return (
    <section className="rover-section-card panel">
      {/* Header */}
      <div className="rover-section-header">
        <div className="rover-header-text">
          <div className="eyebrow">AI INFRASTRUCTURE CO-PILOT</div>
          <h2>Meet Your AI Infrastructure Assistant</h2>
          <p>Your intelligent companion for understanding road conditions, predicting infrastructure failures, and exploring maintenance insights.</p>
        </div>
        <div className="rover-status-pill">
          <span className={`status-dot ${status.configured ? 'green' : 'amber'}`} />
          <span>{status.configured ? `CONNECTED · ${status.provider.toUpperCase()}` : `KEY NEEDED · ${status.provider.toUpperCase()}`}</span>
        </div>
      </div>

      {/* Main Grid: Mascot Left, Chat Right */}
      <div className="rover-layout-grid">
        {/* Left Column: Mascot & Overview */}
        <div className="rover-mascot-side">
          <div className="mascot-frame">
            <img
              src="/assets/rover_mascot.jpg"
              alt="ROVER Road Mascot"
              className="mascot-photo"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
            <div className="mascot-pulse-ring" />
          </div>
          <h3 className="mascot-title">ROVER</h3>
          <div className="mascot-subtitle">Road Operations & Vulnerability Evaluation Robot</div>
          <div className="mascot-speech">
            “Ready for civil analysis. I monitor 2,200 municipal assets across 6 structural categories.”
          </div>

          <div className="rover-overview-blocks">
            <div className="overview-block">
              <strong>🔍 Understand</strong>
              <small>Learn about infrastructure failure prediction and road damage detection.</small>
            </div>
            <div className="overview-block">
              <strong>🗺️ Explore</strong>
              <small>Get guidance on the dashboard's tools, metrics, and visualizations.</small>
            </div>
            <div className="overview-block">
              <strong>⚡ Improve</strong>
              <small>Understand maintenance optimization and model evaluation.</small>
            </div>
          </div>
        </div>

        {/* Right Column: Interactive Chat Interface */}
        <div className="rover-chat-side">
          <div className="chat-control-bar">
            <div className="chat-assistant-meta">
              <span className="chat-avatar-mini">🤖</span>
              <div>
                <strong>ROVER</strong>
                <small>AI Infrastructure Assistant</small>
              </div>
            </div>
            <button type="button" className="chat-reset-btn" onClick={handleReset} title="Clear conversation">
              🗑️ Reset Chat
            </button>
          </div>

          <div className="chat-scroll-area">
            {messages.map((m, idx) => (
              <div key={idx} className={`chat-row ${m.role === 'user' ? 'user-row' : 'rover-row'}`}>
                <div className="bubble-speaker">{m.role === 'user' ? '👤 Highway Engineer' : '🤖 ROVER'}</div>
                <div className="bubble-content" style={{ whiteSpace: 'pre-wrap' }}>
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-row rover-row">
                <div className="bubble-speaker">🤖 ROVER</div>
                <div className="bubble-content typing-indicator">
                  <span>●</span> <span>●</span> <span>●</span> <em>ROVER is analyzing project telemetry...</em>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Question Chips */}
          <div className="chips-title">SUGGESTED QUESTIONS:</div>
          <div className="chips-row">
            {SUGGESTED_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                type="button"
                className="prompt-chip"
                onClick={() => handleSend(prompt)}
                disabled={loading}
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Multiline Input & Send */}
          <div className="chat-input-bar">
            <textarea
              className="chat-textarea"
              rows="2"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask ROVER about infrastructure, road damage, or predictive maintenance... (Press Enter to send, Shift+Enter for new line)"
              disabled={loading}
            />
            <button
              type="button"
              className="chat-send-btn"
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
            >
              Send ✈️
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
