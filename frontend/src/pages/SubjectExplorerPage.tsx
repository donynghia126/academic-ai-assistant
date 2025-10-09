// frontend/src/pages/SubjectExplorerPage.tsx
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import type { Subject } from "../services/apiService";
import { getSubjects } from "../services/apiService";
import "../styles/SubjectExplorerPage.css";

function SubjectExplorerPage() {
  const { t } = useTranslation();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const data = await getSubjects();
        setSubjects(data);
      } catch (err) {
        setError(t("subjectExplorerPage.error"));
      } finally {
        setIsLoading(false);
      }
    };
    fetchSubjects();
  }, [t]);

  if (isLoading) {
    return (
      <div className="explorer-status">{t("subjectExplorerPage.loading")}</div>
    );
  }

  if (error) {
    return <div className="explorer-status error">{error}</div>;
  }

  return (
    <div className="subject-explorer-container">
      <h1>{t("subjectExplorerPage.title")}</h1>
      <div className="subjects-grid">
        {subjects.length > 0 ? (
          subjects.map((subject) => (
            <div key={subject.id} className="subject-card">
              <h2>{subject.name}</h2>
              <p>{subject.description}</p>
              <div className="topics-list">
                <h4>{t("subjectExplorerPage.topicsTitle")}</h4>
                <ul>
                  {subject.topics.map((topic) => (
                    <li key={topic.name}>{topic.name}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))
        ) : (
          <p>{t("subjectExplorerPage.noSubjects")}</p>
        )}
      </div>
    </div>
  );
}

export default SubjectExplorerPage;
