// frontend/src/App.tsx

import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CodeAnalyzerPage from "./pages/CodeAnalyzerPage";
import ChatPage from "./pages/ChatPage"; // << THÊM VÀO
import LanguageSwitcher from "./components/LanguageSwitcher";
import { useTranslation } from "react-i18next";
import "./styles/App.css";

function App() {
  const { t } = useTranslation();

  return (
    <Router>
      <div className="app-container">
        <header className="app-header">
          <nav className="app-nav">
            <div className="nav-links">
              <Link to="/" className="nav-link">
                {t("nav.home")}
              </Link>
              <Link to="/code-analyzer" className="nav-link">
                {t("nav.codeAnalyzer")}
              </Link>
              {/* V << THÊM VÀO V */}
              <Link to="/chat" className="nav-link">
                {t("nav.chat")}
              </Link>
              {/* ^ << THÊM VÀO ^ */}
            </div>
            <div className="language-switcher-container">
              <LanguageSwitcher />
            </div>
          </nav>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/code-analyzer" element={<CodeAnalyzerPage />} />
            {/* V << THÊM VÀO V */}
            <Route path="/chat" element={<ChatPage />} />
            {/* ^ << THÊM VÀO ^ */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
