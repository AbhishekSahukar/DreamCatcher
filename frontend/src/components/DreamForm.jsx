// src/components/DreamForm.jsx
import React, { useState } from "react";
import axios from "axios";
import "../App.css";

export default function DreamForm() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text:
        "Hello! I am DreamCatcher. Tell me your dream and I will dive in deep and Interpret it for you 🌟",
    },
  ]);

  const [isTyping, setIsTyping] = useState(false);

  // 💡 Runtime backend URL resolution
  const API_BASE =
    window.__ENV__?.API_BASE && window.__ENV__.API_BASE.trim() !== ""
      ? window.__ENV__.API_BASE
      : window.location.origin;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const updatedMessages = [...messages, { sender: "user", text: userInput }];
    setMessages(updatedMessages);
    setUserInput("");
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE}/analyse`, {
        dream: userInput,
      });

      const botReply = res.data.interpretation;
      setMessages([...updatedMessages, { sender: "bot", text: botReply }]);
    } catch (error) {
      console.error("API Error:", error);

      setMessages([
        ...updatedMessages,
        { sender: "bot", text: "Something went wrong. Try again." },
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
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}

        {isTyping && (
          <div className="chat-message bot typing">
            DreamCatcher is thinking...
          </div>
        )}
      </div>

      <form className="input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Describe your dream..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />

        <button type="submit">Send</button>
      </form>
    </div>
  );
}
