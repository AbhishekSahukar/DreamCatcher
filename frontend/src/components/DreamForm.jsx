import React, { useState, useRef, useEffect } from "react";
import "../App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function DreamForm() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I am DreamCatcher. Tell me your dream and I will interpret it for you 🌙",
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim() || isTyping) return;

    const userMessage = { sender: "user", text: userInput };
    const botMessage = { sender: "bot", text: "" };

    setMessages((prev) => [...prev, userMessage, botMessage]);
    setUserInput("");
    setIsTyping(true);

    try {
      const res = await fetch(`${API_URL}/analyse`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dream: userInput }),
      });

      if (!res.ok) throw new Error("Server error");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            text: updated[updated.length - 1].text + chunk,
          };
          return updated;
        });
      }
    } catch {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          text: "Something went wrong. Please try again.",
        };
        return updated;
      });
    } finally {
      setIsTyping(false);
    }
  };

  const lastMessage = messages[messages.length - 1];
  const isStreaming = isTyping && lastMessage?.sender === "bot";
  const isWaiting = isStreaming && lastMessage?.text === "";

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => {
          const isLastBot = idx === messages.length - 1 && msg.sender === "bot";
          const showStatus = isLastBot && isStreaming;

          return (
            <div
              key={idx}
              className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              {showStatus && isWaiting ? (
                <span className="status-label">Interpreting your dream...</span>
              ) : (
                msg.text
              )}
            </div>
          );
        })}
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
          {isTyping ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}