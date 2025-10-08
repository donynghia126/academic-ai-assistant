import { useState } from "react";
import axios from "axios";
import { useTranslation } from "react-i18next";
import "../styles/CodeAnalyzerPage.css";

function CodeAnalyzerPage() {
  const { t } = useTranslation();
  const [code, setCode] = useState<string>(
    'function helloWorld() {\n  console.log("Hello, world!");\n}'
  );
  const [explanation, setExplanation] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    setExplanation("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/code/explain",
        {
          code: code,
        }
      );
      setExplanation(response.data.explanation);
    } catch (err: any) {
      console.error("Error calling API:", err);
      const errorMessage =
        err.response?.data?.detail || t("codeAnalyzer.error.generic");
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="code-analyzer-container">
      <h1 className="code-analyzer-title">{t("codeAnalyzer.title")}</h1>
      <p className="code-analyzer-description">{t("codeAnalyzer.description")}</p>

      <form onSubmit={handleSubmit} className="code-analyzer-form">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder={t("codeAnalyzer.placeholder")}
          rows={15}
          className="code-textarea"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading}
          className="submit-button"
        >
          {isLoading
            ? t("codeAnalyzer.button.loading")
            : t("codeAnalyzer.button.submit")}
        </button>
      </form>

      {error && (
        <div className="error-box">
          <h3>{t("codeAnalyzer.error.title")}</h3>
          <p>{error}</p>
        </div>
      )}

      {explanation && (
        <div className="result-box">
          <h3>{t("codeAnalyzer.resultTitle")}</h3>
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
}

export default CodeAnalyzerPage;
