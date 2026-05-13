import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "../App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function DreamForm() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text:
        "Hello! I am DreamCatcher. Tell me your dream and I will interpret it for you 🌙",
    },
  ]);

  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Runtime backend URL resolution
  const API_BASE =
    window.__ENV__?.API_BASE && window.__ENV__.API_BASE.trim() !== ""
      ? window.__ENV__.API_BASE
      : API_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userInput.trim()) return;

    const updatedMessages = [
      ...messages,
      { sender: "user", text: userInput },
    ];

    setMessages(updatedMessages);
    setUserInput("");
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE}/analyse`, {
        dream: userInput,
      });

      const botReply = res.data.interpretation;

      setMessages([
        ...updatedMessages,
        { sender: "bot", text: botReply },
      ]);
    } catch (error) {
      console.error("API Error:", error);

      setMessages([
        ...updatedMessages,
        {
          sender: "bot",
          text: "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${
              msg.sender === "user" ? "user" : "bot"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {isTyping && (
          <div className="chat-message bot typing">
            DreamCatcher is thinking...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Describe your dream..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          disabled={isTyping}
        />

        <button type="submit" disabled={isTyping}>
          Send
        </button>
      </form>
    </div>
  );
}