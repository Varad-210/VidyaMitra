import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// Import connection test in development mode
if (import.meta.env.DEV) {
  import('./utils/connectionTest.js');
}

createRoot(document.getElementById("root")!).render(<App />);
