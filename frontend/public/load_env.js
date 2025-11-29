(function () {
  const script = document.createElement("script");

 
  script.src = window.location.hostname === "localhost"
    ? "/env.js"
    : "/assets/env.js";

  document.head.appendChild(script);
})();
