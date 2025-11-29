
const API_BASE =
  import.meta.env.VITE_API_BASE ||
  window.__ENV__?.API_BASE || 
  `${window.location.origin.replace(/^http/, "http")}:8000`;

export { API_BASE };
