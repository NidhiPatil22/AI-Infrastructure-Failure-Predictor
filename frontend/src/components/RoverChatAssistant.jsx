import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendChatMessage, getChatStatus, getApiErrorMessage } from '../services/api.js';

const INITIAL_MAIN_MENU_CHOICES = [
  {
    id: 'wf_risk',
    label: '1. Analyze Infrastructure Risk',
    description: 'Explore failure predictions, model mechanics, and asset risk tiers',
    action_type: 'workflow',
    workflow: 'infrastructure_risk',
    step: 'options',
  },
  {
    id: 'wf_damage',
    label: '2. Inspect Road Damage',
    description: 'Detect surface distress, cracks, potholes, and review RDI scores',
    action_type: 'workflow',
    workflow: 'road_damage',
    step: 'options',
  },
  {
    id: 'wf_maintenance',
    label: '3. Plan Maintenance',
    description: 'Compare Knapsack algorithms (Hill Climbing, Beam, Tabu Search)',
    action_type: 'workflow',
    workflow: 'plan_maintenance',
    step: 'options',
  },
  {
    id: 'wf_explore',
    label: '4. Explore the Project',
    description: 'Inspect architecture, MLflow logs, AutoML benchmarks, and data structures',
    action_type: 'workflow',
    workflow: 'explore_project',
    step: 'options',
  },
];

const INITIAL_WELCOME = {
  role: 'assistant',
  content:
    '👋 **Hello! I am ROVER — Road Operations & Vulnerability Evaluation Robot.**\n\n' +
    'Your AI assistant for road infrastructure, predictive maintenance, and smarter civil decisions.\n\n' +
    'What would you like to do today? Select one of the guided tasks below, or type any inquiry in the chat:',
};

export default function RoverChatAssistant() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([INITIAL_WELCOME]);
  const [workflow, setWorkflow] = useState('main');
  const [step, setStep] = useState('menu');
  const [choices, setChoices] = useState(INITIAL_MAIN_MENU_CHOICES);
  const [selectedChoiceId, setSelectedChoiceId] = useState(null);
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
  }, [messages, choices, loading]);

  // Handle clicking a structured option card
  const handleSelectChoice = async (choice) => {
    if (loading) return;
    setSelectedChoiceId(choice.id);

    // If this choice triggers actual application navigation
    if (choice.action_type === 'navigate' && choice.payload?.route) {
      navigate(choice.payload.route);
      return;
    }

    const userMsg = { role: 'user', content: `Selected: **${choice.label}**` };
    const nextHistory = [...messages, userMsg];
    setMessages(nextHistory);
    setLoading(true);

    try {
      const historyPayload = nextHistory
        .slice(-8)
        .map((m) => ({ role: m.role, content: m.content }));

      const response = await sendChatMessage(
        null,
        historyPayload,
        null,
        choice.workflow || workflow,
        choice.step || step,
        choice.id
      );

      // If backend returned a real navigation action
      if (response.action_executed === 'navigate' && response.action_data?.route) {
        navigate(response.action_data.route);
        return;
      }

      setWorkflow(response.workflow || workflow);
      setStep(response.step || step);
      setChoices(response.choices || INITIAL_MAIN_MENU_CHOICES);
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
      setSelectedChoiceId(null);
    }
  };

  // Back button handler
  const handleBack = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await sendChatMessage(null, [], null, workflow, step, 'back');
      setWorkflow(response.workflow || 'main');
      setStep(response.step || 'menu');
      setChoices(response.choices || INITIAL_MAIN_MENU_CHOICES);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.response || 'Returned to previous options.' },
      ]);
    } catch (err) {
      setWorkflow('main');
      setStep('menu');
      setChoices(INITIAL_MAIN_MENU_CHOICES);
    } finally {
      setLoading(false);
    }
  };

  // Main Menu / Home handler
  const handleHome = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await sendChatMessage(null, [], null, 'main', 'menu', 'menu');
      setWorkflow('main');
      setStep('menu');
      setChoices(INITIAL_MAIN_MENU_CHOICES);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.response || INITIAL_WELCOME.content },
      ]);
    } catch (err) {
      setWorkflow('main');
      setStep('menu');
      setChoices(INITIAL_MAIN_MENU_CHOICES);
    } finally {
      setLoading(false);
    }
  };

  // Free-text send handler
  const handleSend = async () => {
    const prompt = input.trim();
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

      const response = await sendChatMessage(prompt, historyPayload, null, workflow, step, null);
      setWorkflow(response.workflow || workflow);
      setStep(response.step || 'follow_up');
      if (response.choices && response.choices.length > 0) {
        setChoices(response.choices);
      }
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
    setWorkflow('main');
    setStep('menu');
    setChoices(INITIAL_MAIN_MENU_CHOICES);
  };

  const isInSubstep = workflow !== 'main' || step !== 'menu';

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
          <span>{status.configured ? `CONNECTED · ${status.provider.toUpperCase()}` : `TASK-MODE READY · ${status.provider.toUpperCase()}`}</span>
        </div>
      </div>

      {/* Main Grid: Mascot Left, Guided Chat Right */}
      <div className="rover-layout-grid">
        {/* Left Column: Mascot & Overview */}
        <div className="rover-mascot-side">
          <div className="mascot-frame">
            <img
              src="/assets/rover_mascot.jpg"
              alt="ROVER Road Mascot"
              className="mascot-photo"
              onError={(e) => {
                e.target.src = '/assets/rover_avatar.jpg';
              }}
            />
            <div className="mascot-pulse-ring" />
          </div>
          <h3 className="mascot-title">ROVER</h3>
          <div className="mascot-subtitle">Road Operations & Vulnerability Evaluation Robot</div>
          <div className="mascot-speech">
            “Hello! I am ROVER 👋 Your AI assistant for road infrastructure, predictive maintenance and smarter decisions.”
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

        {/* Right Column: Interactive Guided Chat */}
        <div className="rover-chat-side">
          <div className="chat-control-bar">
            <div className="chat-assistant-meta">
              <span className="chat-avatar-mini">🤖</span>
              <div>
                <strong>ROVER</strong>
                <small>Guided Task Assistant · Workflow: {workflow.replace('_', ' ').toUpperCase()}</small>
              </div>
            </div>
            <div className="workflow-nav-controls">
              {isInSubstep && (
                <button type="button" className="chat-ctrl-btn" onClick={handleBack} title="Back to previous step">
                  ↩️ Back
                </button>
              )}
              <button type="button" className="chat-ctrl-btn" onClick={handleHome} title="Return to Main Menu">
                🏠 Main Menu
              </button>
              <button type="button" className="chat-ctrl-btn" onClick={handleReset} title="Clear conversation">
                🗑️ Reset
              </button>
            </div>
          </div>

          {/* Conversation History Area */}
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

          {/* Interactive Guided Choice Cards (Requirement 1 & 2) */}
          {choices && choices.length > 0 && (
            <div className="guided-choices-section">
              <div className="chips-title">👉 SELECT A GUIDED TASK OPTION:</div>
              <div className="guided-choices-grid">
                {choices.map((choice) => (
                  <button
                    key={choice.id}
                    type="button"
                    className={`guided-choice-card ${selectedChoiceId === choice.id ? 'active' : ''}`}
                    onClick={() => handleSelectChoice(choice)}
                    disabled={loading}
                  >
                    <div className="choice-card-header">
                      <strong>{choice.label}</strong>
                      {choice.action_type === 'navigate' && <span className="action-tag">OPEN ↗</span>}
                    </div>
                    {choice.description && <p className="choice-card-desc">{choice.description}</p>}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Multiline Free-Chat Input Bar (Requirement 3: free chat supported at any time) */}
          <div className="chat-input-bar">
            <textarea
              className="chat-textarea"
              rows="2"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask ROVER any question, or select a guided task above... (Enter to send, Shift+Enter for newline)"
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
