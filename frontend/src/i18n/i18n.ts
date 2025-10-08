import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import translationEN from "./en.json";
import translationVI from "./vi.json";
import translationJA from "./ja.json";

const resources = {
  en: {
    translation: translationEN,
  },
  vi: {
    translation: translationVI,
  },
  ja: {
    translation: translationJA,
  },
};

i18n
  .use(LanguageDetector) // Tự động phát hiện ngôn ngữ của trình duyệt
  .use(initReactI18next) // Kết nối i18next với react
  .init({
    resources,
    fallbackLng: "en", // Ngôn ngữ mặc định nếu không phát hiện được
    interpolation: {
      escapeValue: false, // React đã tự chống XSS
    },
    detection: {
      order: ["localStorage", "navigator"], // Ưu tiên ngôn ngữ đã lưu, sau đó đến ngôn ngữ trình duyệt
    },
  });

export default i18n;
