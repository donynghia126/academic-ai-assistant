import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { checkHealth } from "../services/apiService";
import "../styles/HomePage.css";

function HomePage() {
  const { t } = useTranslation();
  const [statusMessage, setStatusMessage] = useState(
    t("backendStatus.connecting")
  );
  const [statusType, setStatusType] = useState<
    "connecting" | "connected" | "error"
  >("connecting");

  useEffect(() => {
    const getApiStatus = async () => {
      try {
        const data = await checkHealth();
        setStatusMessage(t("backendStatus.ok", { message: data.message }));
        setStatusType("connected");
      } catch (error) {
        setStatusMessage(t("backendStatus.error"));
        setStatusType("error");
      }
    };

    getApiStatus();
  }, [t]);

  return (
    <div className="home-page-container">
      <h1 className="home-title">{t("title")}</h1>

      <div className="home-content">
        <div className="status-container">
          <span className="status-label">{t("backendStatus.label")}</span>
          <span className={`status-message ${statusType}`}>
            {statusMessage}
          </span>
          <span className={`status-icon ${statusType}`}></span>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
