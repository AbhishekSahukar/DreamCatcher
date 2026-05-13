import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "../App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function DreamForm() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
<<<<<<< HEAD
      text:
        "Hello! I am DreamCatcher. Tell me your dream and I will dive in deep and Interpret it for you 🌟",
=======
      text: "Hello! I am DreamCatcher. Tell me your dream and I will interpret it for you 🌙",
>>>>>>> 142df6a (Readme and code fix)
    },
  ]);

  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

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
<<<<<<< HEAD
      const res = await axios.post(`${API_BASE}/analyse`, {
        dream: userInput,
      });

      const botReply = res.data.interpretation;
      setMessages([...updatedMessages, { sender: "bot", text: botReply }]);
    } catch (error) {
      console.error("API Error:", error);

=======
      const res = await axios.post(`${API_URL}/analyse`, { dream: userInput });
      setMessages([...updatedMessages, { sender: "bot", text: res.data.interpretation }]);
    } catch {
>>>>>>> 142df6a (Readme and code fix)
      setMessages([
        ...updatedMessages,
        { sender: "bot", text: "Something went wrong. Please try again." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}>
            {msg.text}
          </div>
        ))}
        {isTyping && (
<<<<<<< HEAD
          <div className="chat-message bot typing">
            DreamCatcher is thinking...
          </div>
=======
          <div className="chat-message bot typing">DreamCatcher is thinking...</div>
>>>>>>> 142df6a (Readme and code fix)
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
<<<<<<< HEAD

        <button type="submit">Send</button>
=======
        <button type="submit" disabled={isTyping}>
          Send
        </button>
>>>>>>> 142df6a (Readme and code fix)
      </form>
    </div>
  );
}
