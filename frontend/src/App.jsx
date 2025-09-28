// src/App.jsx
import React from "react";
import DreamForm from "./components/DreamForm";
import "./App.css";

export default function App() {
  return (
    <div className="app-container">
      <h1 className="title">DreamCatcher</h1>
      <DreamForm />
    </div>
  );
}
