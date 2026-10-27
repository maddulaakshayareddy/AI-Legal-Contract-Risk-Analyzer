import { useEffect, useMemo, useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const SUPPORTED_LANGUAGES = [
  "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi",
  "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam",
  "Manipuri", "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit",
  "Santali", "Sindhi", "Tamil", "Telugu", "Urdu",
  "Bhojpuri", "Rajasthani", "Tulu", "Awadhi", "Magahi",
  "Chhattisgarhi", "Haryanvi", "Marwari", "Garhwali", "Kumaoni",
  "Bundeli", "Mewari", "English", "Spanish", "French", "German", "Arabic",
];

const SPEECH_LANGUAGE_CODES = {
  Assamese: "as-IN", Bengali: "bn-IN", Bodo: "brx-IN", Dogri: "doi-IN",
  Gujarati: "gu-IN", Hindi: "hi-IN", Kannada: "kn-IN", Kashmiri: "ks-IN",
  Konkani: "kok-IN", Maithili: "mai-IN", Malayalam: "ml-IN", Manipuri: "mni-IN",
  Marathi: "mr-IN", Nepali: "ne-NP", Odia: "or-IN", Punjabi: "pa-IN",
  Sanskrit: "sa-IN", Santali: "sat-IN", Sindhi: "sd-IN", Tamil: "ta-IN",
  Telugu: "te-IN", Urdu: "ur-IN", Bhojpuri: "hi-IN", Rajasthani: "hi-IN",
  Tulu: "kn-IN", Awadhi: "hi-IN", Magahi: "hi-IN", Chhattisgarhi: "hi-IN",
  Haryanvi: "hi-IN", Marwari: "hi-IN", Garhwali: "hi-IN", Kumaoni: "hi-IN",
  Bundeli: "hi-IN", Mewari: "hi-IN", English: "en-IN", Spanish: "es-ES",
  French: "fr-FR", German: "de-DE", Arabic: "ar-SA",
};

const getSpeechLanguageCode = (language) => SPEECH_LANGUAGE_CODES[language] || "en-IN";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [recoveryCode, setRecoveryCode] = useState("");
  const [resetLoading, setResetLoading] = useState(false);
  const [authMessage, setAuthMessage] = useState("");
  const [authMessageType, setAuthMessageType] = useState("danger");
  const [loading, setLoading] = useState(false);

  const [recoveryMessage, setRecoveryMessage] = useState("");
  const [recoveryLoading, setRecoveryLoading] = useState(false);
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("user") || "null")
  );

  const [activePage, setActivePage] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [contracts, setContracts] = useState([]);
  const [analysisHistory, setAnalysisHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  const [fileTitle, setFileTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadStage, setUploadStage] = useState("");

  const [scanFile, setScanFile] = useState(null);
  const [uploadingScan, setUploadingScan] = useState(false);
  const [scanMessage, setScanMessage] = useState("");
  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const cameraVideoRef = useRef(null);
  const cameraStreamRef = useRef(null);
  const speechRecognitionRef = useRef(null);

  const [contractTitle, setContractTitle] = useState("");
  const [contractText, setContractText] = useState("");
  const [creatingContract, setCreatingContract] = useState(false);
  const [contractMessage, setContractMessage] = useState("");

  const [selectedContract, setSelectedContract] = useState(null);
  const [loadingContract, setLoadingContract] = useState(false);

  const [analysis, setAnalysis] = useState(null);
  const [analyzingId, setAnalyzingId] = useState(null);
  const [analysisError, setAnalysisError] = useState("");
  const [evidenceSources, setEvidenceSources] = useState([]);
  const [evidenceLoading, setEvidenceLoading] = useState(false);
  const [evidenceError, setEvidenceError] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);
  const [auditLoading, setAuditLoading] = useState(false);
  const [auditError, setAuditError] = useState("");

  const [qaContractId, setQaContractId] = useState("");
  const [question, setQuestion] = useState("");
  const [qaAnswer, setQaAnswer] = useState(null);
  const [qaLoading, setQaLoading] = useState(false);
  const [qaError, setQaError] = useState("");

  const [reportLoading, setReportLoading] = useState("");
  const [reportMessage, setReportMessage] = useState("");

  const [documentType, setDocumentType] = useState("Non-Disclosure Agreement");
  const [documentDetails, setDocumentDetails] = useState("");
  const [documentGeneratedContent, setDocumentGeneratedContent] = useState("");
  const [documentGeneratedSourceContent, setDocumentGeneratedSourceContent] = useState("");
  const [documentOutputLanguage, setDocumentOutputLanguage] = useState("English");
  const [documentTranslating, setDocumentTranslating] = useState(false);
  const [documentGenerating, setDocumentGenerating] = useState(false);
  const [documentGeneratorMessage, setDocumentGeneratorMessage] = useState("");
  const [documentVoiceLanguage, setDocumentVoiceLanguage] = useState("English");
  const [documentVoiceListening, setDocumentVoiceListening] = useState(false);
  const [documentSpeaking, setDocumentSpeaking] = useState(false);
  const [availableVoices, setAvailableVoices] = useState([]);
  const documentVoiceRecognitionRef = useRef(null);
  const [documentReferenceFileLoading, setDocumentReferenceFileLoading] = useState(false);
  const [documentReferenceFileName, setDocumentReferenceFileName] = useState("");

  useEffect(() => {
    if (!window.speechSynthesis) return;

    const loadVoices = () => {
      setAvailableVoices(window.speechSynthesis.getVoices() || []);
    };

    loadVoices();
    window.speechSynthesis.addEventListener("voiceschanged", loadVoices);

    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", loadVoices);
    };
  }, []);

  const [clauseA, setClauseA] = useState("");
  const [clauseB, setClauseB] = useState("");
  const [clauseComparison, setClauseComparison] = useState("");
  const [clauseComparing, setClauseComparing] = useState(false);
  const [clauseComparisonMessage, setClauseComparisonMessage] = useState("");
  const [clauseAFileLoading, setClauseAFileLoading] = useState(false);
  const [clauseAFileName, setClauseAFileName] = useState("");
  const [clauseBFileLoading, setClauseBFileLoading] = useState(false);
  const [clauseBFileName, setClauseBFileName] = useState("");

  const [versionA, setVersionA] = useState("");
  const [versionB, setVersionB] = useState("");
  const [versionAName, setVersionAName] = useState("");
  const [versionBName, setVersionBName] = useState("");
  const [versionAFileLoading, setVersionAFileLoading] = useState(false);
  const [versionBFileLoading, setVersionBFileLoading] = useState(false);
  const [versionDiff, setVersionDiff] = useState(null);
  const [versionDiffLoading, setVersionDiffLoading] = useState(false);
  const [versionDiffMessage, setVersionDiffMessage] = useState("");

  const [obligationsContractId, setObligationsContractId] = useState("");
  const [obligationsResult, setObligationsResult] = useState(null);
  const [obligationsLoading, setObligationsLoading] = useState(false);
  const [obligationsMessage, setObligationsMessage] = useState("");

  const [languageText, setLanguageText] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState("English");
  const [targetLanguage, setTargetLanguage] = useState("Telugu");
  const [translatedText, setTranslatedText] = useState("");
  const [translating, setTranslating] = useState(false);
  const [translationMessage, setTranslationMessage] = useState("");
  const [languageFileLoading, setLanguageFileLoading] = useState(false);
  const [languageFileName, setLanguageFileName] = useState("");
  const [translationDownloadLoading, setTranslationDownloadLoading] = useState("");
  const [languageVoiceListening, setLanguageVoiceListening] = useState(false);
  const [languageSpeaking, setLanguageSpeaking] = useState(false);
  const languageVoiceRecognitionRef = useRef(null);

  const [assistantOpen, setAssistantOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [aboutModal, setAboutModal] = useState("");
  const [voiceListening, setVoiceListening] = useState(false);
  const [speakingAnswer, setSpeakingAnswer] = useState(false);

  const uploadLanguageFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";

    if (!file) return;

    setTranslationMessage("");
    setTranslatedText("");
    setLanguageFileLoading(true);
    setLanguageFileName(file.name);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const auth = token();

      const response = await fetch(`${API_URL}/api/language/translate-file`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${auth}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not read the document.");
      }

      setLanguageText(data.extracted_text || "");
      setTranslationMessage(
        data.extracted_text
          ? `Document loaded: ${file.name}`
          : "The document was read, but no text was found."
      );
    } catch (error) {
      setLanguageText("");
      setLanguageFileName("");
      setTranslationMessage(error.message);
    } finally {
      setLanguageFileLoading(false);
    }
  };

  const translateText = async (e) => {
    e?.preventDefault();
    setTranslationMessage("");

    if (!languageText.trim()) {
      setTranslationMessage("Please enter some text to translate.");
      return;
    }

    setTranslating(true);
    setTranslatedText("");

    try {
      const auth = token();

      const response = await fetch(`${API_URL}/api/language/translate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          text: languageText.trim(),
          source_language: sourceLanguage,
          target_language: targetLanguage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Translation failed.");
      }

      setTranslatedText(data.translated_text || "");
      setTranslationMessage("Translation completed successfully.");
    } catch (error) {
      setTranslationMessage(error.message);
    } finally {
      setTranslating(false);
    }
  };

  const copyTranslatedText = async () => {
    if (!translatedText) return;

    try {
      await navigator.clipboard.writeText(translatedText);
      setTranslationMessage("Translation copied to your clipboard.");
    } catch {
      setTranslationMessage("Could not copy automatically. Please copy the text manually.");
    }
  };

  const downloadTranslatedFile = async (format) => {
    if (!translatedText) return;

    setTranslationMessage("");
    setTranslationDownloadLoading(format);

    try {
      const endpoint = format === "pdf" ? "download-pdf" : "download-docx";
      const auth = token();

      const response = await fetch(`${API_URL}/api/language/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          translated_text: translatedText,
          target_language: targetLanguage,
        }),
      });

      if (!response.ok) {
        let message = "Could not download the translated document.";
        try {
          const data = await response.json();
          message = data.detail || message;
        } catch {
          // Keep the default message when the server does not return JSON.
        }
        throw new Error(message);
      }

      const blob = await response.blob();
      const extension = format === "pdf" ? "pdf" : "docx";
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `translated_contract_${targetLanguage.toLowerCase().replace(/\s+/g, "_")}.${extension}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(link.href);
      setTranslationMessage(`Translated ${format.toUpperCase()} downloaded successfully.`);
    } catch (error) {
      setTranslationMessage(error.message);
    } finally {
      setTranslationDownloadLoading("");
    }
  };

  const stopLanguageVoiceInput = () => {
    if (languageVoiceRecognitionRef.current) {
      try {
        languageVoiceRecognitionRef.current.stop();
      } catch {}
    }
    languageVoiceRecognitionRef.current = null;
    setLanguageVoiceListening(false);
  };

  const stopLanguageSpeech = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setLanguageSpeaking(false);
  };

  const startLanguageVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setTranslationMessage("Voice input is not supported in this browser. You can type the text instead.");
      return;
    }
    if (languageVoiceListening) {
      stopLanguageVoiceInput();
      return;
    }
    stopLanguageSpeech();
    const recognition = new SpeechRecognition();
    recognition.lang = getSpeechLanguageCode(sourceLanguage);
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onstart = () => setLanguageVoiceListening(true);
    recognition.onend = () => {
      languageVoiceRecognitionRef.current = null;
      setLanguageVoiceListening(false);
    };
    recognition.onerror = (event) => {
      languageVoiceRecognitionRef.current = null;
      setLanguageVoiceListening(false);
      if (event?.error !== "aborted") setTranslationMessage("Voice input could not be captured. Please try again or type the text.");
    };
    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript || "";
      if (transcript.trim()) {
        setLanguageText((previous) => previous ? `${previous} ${transcript.trim()}` : transcript.trim());
        setLanguageFileName("");
      }
    };
    languageVoiceRecognitionRef.current = recognition;
    recognition.start();
  };

  const speakTranslatedText = () => {
    if (!translatedText || !window.speechSynthesis) {
      setTranslationMessage("Voice playback is not supported in this browser.");
      return;
    }
    if (languageSpeaking) {
      stopLanguageSpeech();
      return;
    }
    stopLanguageVoiceInput();
    window.speechSynthesis.cancel();
    const selectedVoice = findSpeechVoice(targetLanguage);
    if (!selectedVoice) {
      setTranslationMessage(
        `No ${targetLanguage} voice is available in your browser/device. Please install a ${targetLanguage} text-to-speech voice in Windows, or choose another available language.`
      );
      return;
    }

    const utterance = new SpeechSynthesisUtterance(translatedText);
    utterance.lang = getSpeechLanguageCode(targetLanguage);
    utterance.voice = selectedVoice;
    utterance.rate = 0.9;
    utterance.onstart = () => setLanguageSpeaking(true);
    utterance.onend = () => setLanguageSpeaking(false);
    utterance.onerror = () => setLanguageSpeaking(false);
    setLanguageSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const token = () => localStorage.getItem("access_token");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setAuthMessage("");
    setAuthMessageType("danger");

    const newPassword = form.password;

    if (!form.email.trim()) {
      setAuthMessage("Please enter your account email.");
      return;
    }

    if (!recoveryCode.trim()) {
      setAuthMessage("Please enter your recovery code.");
      return;
    }

    const strongPassword =
      newPassword.length >= 8 &&
      /[A-Z]/.test(newPassword) &&
      /[a-z]/.test(newPassword) &&
      /\d/.test(newPassword) &&
      /[^A-Za-z0-9]/.test(newPassword);

    if (!strongPassword) {
      setAuthMessage(
        "New password must be at least 8 characters and include uppercase, lowercase, number, and special character."
      );
      return;
    }

    if (newPassword !== confirmPassword) {
      setAuthMessage("Passwords do not match.");
      return;
    }

    setResetLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/password/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: form.email,
          recovery_code: recoveryCode,
          new_password: newPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not reset your password.");
      }

      setAuthMessage(data.message || "Password reset successfully.");
      setAuthMessageType("success");
      setIsForgotPassword(false);
      setIsLogin(true);
      setRecoveryCode("");
      setConfirmPassword("");
      setForm((prev) => ({ ...prev, password: "" }));
      setShowPassword(false);
      setShowConfirmPassword(false);
    } catch (error) {
      setAuthMessage(error.message);
      setAuthMessageType("danger");
    } finally {
      setResetLoading(false);
    }
  };

  const generateRecoveryCode = async () => {
    const auth = token();
    if (!auth) return;

    setRecoveryLoading(true);
    setRecoveryMessage("");

    try {
      const response = await fetch(`${API_URL}/api/password/generate-code`, {
        method: "POST",
        headers: { Authorization: `Bearer ${auth}` },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not generate a recovery code.");
      }

      setRecoveryCode(data.recovery_code || "");
      setRecoveryMessage(
        "Recovery code generated. Save it somewhere secure. Generating a new code will replace the previous one."
      );
    } catch (error) {
      setRecoveryMessage(error.message);
    } finally {
      setRecoveryLoading(false);
    }
  };

  const copyRecoveryCode = async () => {
    if (!recoveryCode) return;

    try {
      await navigator.clipboard.writeText(recoveryCode);
      setRecoveryMessage("Recovery code copied to your clipboard.");
    } catch {
      setRecoveryMessage("Could not copy automatically. Please copy the code manually.");
    }
  };

  const extractProjectDocument = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const auth = token();

    const response = await fetch(`${API_URL}/api/language/translate-file`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${auth}`,
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Could not read the document.");
    }

    return data.extracted_text || "";
  };

  const stopDocumentVoiceInput = () => {
    if (documentVoiceRecognitionRef.current) {
      try {
        documentVoiceRecognitionRef.current.stop();
      } catch {}
    }
    documentVoiceRecognitionRef.current = null;
    setDocumentVoiceListening(false);
  };

  const findSpeechVoice = (language) => {
    const languageCode = getSpeechLanguageCode(language);
    const normalizedCode = languageCode.toLowerCase();
    const baseCode = normalizedCode.split("-")[0];

    return (
      availableVoices.find(
        (voice) => voice.lang?.toLowerCase() === normalizedCode
      ) ||
      availableVoices.find(
        (voice) => voice.lang?.toLowerCase().startsWith(`${baseCode}-`)
      ) ||
      null
    );
  };

  const speakGeneratedDocument = () => {
    if (!documentGeneratedContent || !window.speechSynthesis) {
      setDocumentGeneratorMessage("Voice playback is not supported in this browser.");
      return;
    }

    if (documentSpeaking) {
      window.speechSynthesis.cancel();
      setDocumentSpeaking(false);
      return;
    }

    stopDocumentVoiceInput();
    window.speechSynthesis.cancel();

    const languageCode = getSpeechLanguageCode(documentOutputLanguage);
    const selectedVoice = findSpeechVoice(documentOutputLanguage);

    if (!selectedVoice) {
      setDocumentGeneratorMessage(
        `No ${documentOutputLanguage} voice is available in your browser/device. Please install a ${documentOutputLanguage} text-to-speech voice in Windows, or choose another available language.`
      );
      return;
    }

    const utterance = new SpeechSynthesisUtterance(documentGeneratedContent);
    utterance.lang = languageCode;
    utterance.voice = selectedVoice;
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    utterance.onstart = () => {
      setDocumentSpeaking(true);
      setDocumentGeneratorMessage(
        `Speaking in ${documentOutputLanguage}...`
      );
    };

    utterance.onend = () => {
      setDocumentSpeaking(false);
    };

    utterance.onerror = () => {
      setDocumentSpeaking(false);
      setDocumentGeneratorMessage(
        `Could not play the ${documentOutputLanguage} voice.`
      );
    };

    setDocumentSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const startDocumentVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setDocumentGeneratorMessage("Voice input is not supported in this browser. You can type the requirements instead.");
      return;
    }
    if (documentVoiceListening) {
      stopDocumentVoiceInput();
      return;
    }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setDocumentSpeaking(false);
    const recognition = new SpeechRecognition();
    recognition.lang = getSpeechLanguageCode(documentVoiceLanguage);
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onstart = () => setDocumentVoiceListening(true);
    recognition.onend = () => {
      documentVoiceRecognitionRef.current = null;
      setDocumentVoiceListening(false);
    };
    recognition.onerror = (event) => {
      documentVoiceRecognitionRef.current = null;
      setDocumentVoiceListening(false);
      if (event?.error !== "aborted") setDocumentGeneratorMessage("Voice input could not be captured. Please try again or type the requirements.");
    };
    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript || "";
      if (transcript.trim()) {
        setDocumentDetails((previous) => previous ? `${previous} ${transcript.trim()}` : transcript.trim());
        setDocumentReferenceFileName("");
      }
    };
    documentVoiceRecognitionRef.current = recognition;
    recognition.start();
  };

  const uploadDocumentReferenceFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    setDocumentGeneratorMessage("");
    setDocumentReferenceFileLoading(true);
    setDocumentReferenceFileName(file.name);

    try {
      const extractedText = await extractProjectDocument(file);
      if (!extractedText.trim()) {
        throw new Error("No selectable text was found in this document. For a scanned/image-only PDF, use the Scan feature first.");
      }
      setDocumentDetails(extractedText);
      setDocumentGeneratorMessage(`Reference document loaded: ${file.name}`);
    } catch (error) {
      setDocumentReferenceFileName("");
      setDocumentGeneratorMessage(error.message);
    } finally {
      setDocumentReferenceFileLoading(false);
    }
  };

  const uploadClauseFile = async (e, clause) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    setClauseComparisonMessage("");
    if (clause === "A") {
      setClauseAFileLoading(true);
      setClauseAFileName(file.name);
    } else {
      setClauseBFileLoading(true);
      setClauseBFileName(file.name);
    }

    try {
      const extractedText = await extractProjectDocument(file);
      if (!extractedText.trim()) {
        throw new Error("No selectable text was found in this document. For a scanned/image-only PDF, use the Scan feature first.");
      }

      if (clause === "A") {
        setClauseA(extractedText);
        setClauseAFileName(file.name);
      } else {
        setClauseB(extractedText);
        setClauseBFileName(file.name);
      }
      setClauseComparisonMessage(`Document loaded: ${file.name}. Review the text and compare it.`);
    } catch (error) {
      if (clause === "A") {
        setClauseAFileName("");
      } else {
        setClauseBFileName("");
      }
      setClauseComparisonMessage(error.message);
    } finally {
      if (clause === "A") {
        setClauseAFileLoading(false);
      } else {
        setClauseBFileLoading(false);
      }
    }
  };

  const generateDocument = async (e) => {
    e?.preventDefault();
    setDocumentGeneratorMessage("");

    if (!documentType.trim()) {
      setDocumentGeneratorMessage("Please select a document type.");
      return;
    }

    if (!documentDetails.trim() || documentDetails.trim().length < 10) {
      setDocumentGeneratorMessage("Please describe the document details in at least 10 characters.");
      return;
    }

    setDocumentGenerating(true);
    setDocumentGeneratedContent("");

    try {
      const auth = token();

      const response = await fetch(`${API_URL}/api/document-generator/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          document_type: documentType.trim(),
          details: documentDetails.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not generate the document.");
      }

      const generatedContent = data.content || "";
      setDocumentGeneratedSourceContent(generatedContent);

      if (documentOutputLanguage === "English") {
        setDocumentGeneratedContent(generatedContent);
        setDocumentGeneratorMessage("Document generated successfully.");
      } else {
        setDocumentTranslating(true);
        setDocumentGeneratorMessage(`Document generated. Translating to ${documentOutputLanguage}...`);

        try {
          const translationResponse = await fetch(`${API_URL}/api/language/translate`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${auth}`,
            },
            body: JSON.stringify({
              text: generatedContent,
              source_language: "English",
              target_language: documentOutputLanguage,
            }),
          });

          const translationData = await translationResponse.json();

          if (!translationResponse.ok) {
            throw new Error(translationData.detail || "Document translation failed.");
          }

          setDocumentGeneratedContent(translationData.translated_text || generatedContent);
          setDocumentGeneratorMessage(`Document generated in ${documentOutputLanguage}.`);
        } catch (translationError) {
          setDocumentGeneratedContent(generatedContent);
          setDocumentGeneratorMessage(`Document generated in English. Translation failed: ${translationError.message}`);
        } finally {
          setDocumentTranslating(false);
        }
      }
    } catch (error) {
      setDocumentGeneratorMessage(error.message);
    } finally {
      setDocumentGenerating(false);
    }
  };

  const changeDocumentOutputLanguage = async (language) => {
    setDocumentOutputLanguage(language);

    if (!documentGeneratedSourceContent) {
      return;
    }

    if (language === "English") {
      setDocumentGeneratedContent(documentGeneratedSourceContent);
      setDocumentGeneratorMessage("Document language changed to English.");
      return;
    }

    setDocumentTranslating(true);
    setDocumentGeneratorMessage(`Translating document to ${language}...`);

    try {
      const auth = token();
      const response = await fetch(`${API_URL}/api/language/translate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          text: documentGeneratedSourceContent,
          source_language: "English",
          target_language: language,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Document translation failed.");
      }

      setDocumentGeneratedContent(data.translated_text || documentGeneratedSourceContent);
      setDocumentGeneratorMessage(`Document translated to ${language}.`);
    } catch (error) {
      setDocumentGeneratorMessage(`Could not translate the document: ${error.message}`);
    } finally {
      setDocumentTranslating(false);
    }
  };

  const copyGeneratedDocument = async () => {
    if (!documentGeneratedContent) return;

    try {
      await navigator.clipboard.writeText(documentGeneratedContent);
      setDocumentGeneratorMessage("Generated document copied to your clipboard.");
    } catch {
      setDocumentGeneratorMessage("Could not copy automatically. Please select and copy the document manually.");
    }
  };

  const downloadGeneratedDocument = async () => {
    if (!documentGeneratedContent) return;

    setDocumentGeneratorMessage("Preparing PDF...");

    try {
      const auth = token();

      const response = await fetch(`${API_URL}/api/language/download-pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          translated_text: documentGeneratedContent,
          target_language: documentOutputLanguage,
        }),
      });

      if (!response.ok) {
        let message = "Could not generate the PDF.";

        try {
          const data = await response.json();
          message = data.detail || message;
        } catch {}

        throw new Error(message);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${documentType.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_") || "generated_document"}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setDocumentGeneratorMessage("PDF downloaded successfully.");
    } catch (error) {
      setDocumentGeneratorMessage(error.message);
    }
  };

  const compareClauses = async (e) => {
    e?.preventDefault();
    setClauseComparisonMessage("");

    if (!clauseA.trim() || clauseA.trim().length < 10) {
      setClauseComparisonMessage("Please enter Clause A with at least 10 characters.");
      return;
    }

    if (!clauseB.trim() || clauseB.trim().length < 10) {
      setClauseComparisonMessage("Please enter Clause B with at least 10 characters.");
      return;
    }

    setClauseComparing(true);
    setClauseComparison("");

    try {
      const auth = token();

      const response = await fetch(`${API_URL}/api/clause-comparison/compare`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          clause_a: clauseA.trim(),
          clause_b: clauseB.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not compare the clauses.");
      }

      setClauseComparison(data.comparison || "");
      setClauseComparisonMessage("Clauses compared successfully.");
    } catch (error) {
      setClauseComparisonMessage(error.message);
    } finally {
      setClauseComparing(false);
    }
  };


  const uploadVersionFile = async (e, version) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    setVersionDiffMessage("");
    if (version === "A") {
      setVersionAFileLoading(true);
      setVersionAName(file.name);
    } else {
      setVersionBFileLoading(true);
      setVersionBName(file.name);
    }

    try {
      const extractedText = await extractProjectDocument(file);
      if (!extractedText.trim()) {
        throw new Error("No readable text was found in this document.");
      }

      if (version === "A") {
        setVersionA(extractedText);
      } else {
        setVersionB(extractedText);
      }
      setVersionDiff(null);
      setVersionDiffMessage(`${file.name} loaded successfully.`);
    } catch (error) {
      if (version === "A") setVersionAName("");
      else setVersionBName("");
      setVersionDiffMessage(error.message);
    } finally {
      if (version === "A") setVersionAFileLoading(false);
      else setVersionBFileLoading(false);
    }
  };

  const compareContractVersions = async (e) => {
    e?.preventDefault();
    setVersionDiffMessage("");

    if (!versionA.trim() || versionA.trim().length < 20) {
      setVersionDiffMessage("Please provide Version 1 with at least 20 characters.");
      return;
    }
    if (!versionB.trim() || versionB.trim().length < 20) {
      setVersionDiffMessage("Please provide Version 2 with at least 20 characters.");
      return;
    }

    setVersionDiffLoading(true);
    setVersionDiff(null);

    try {
      const auth = token();

      const response = await fetch(`${API_URL}/api/version-diff/compare`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          document_a: versionA.trim(),
          document_b: versionB.trim(),
          title_a: versionAName || "Version 1",
          title_b: versionBName || "Version 2",
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Could not compare the contract versions.");
      }

      setVersionDiff(data);
      setVersionDiffMessage("Contract versions compared successfully.");
    } catch (error) {
      setVersionDiffMessage(error.message);
    } finally {
      setVersionDiffLoading(false);
    }
  };

  const extractObligations = async () => {
    setObligationsMessage("");
    setObligationsResult(null);

    if (!obligationsContractId) {
      setObligationsMessage("Please select a contract first.");
      return;
    }

    setObligationsLoading(true);

    try {
      const auth = token();
      const contractResponse = await fetch(`${API_URL}/api/contracts/${obligationsContractId}`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      const contractData = await contractResponse.json();

      if (!contractResponse.ok) {
        throw new Error(contractData.detail || "Could not load the selected contract.");
      }

      const contractTextValue = contractData.raw_text || "";
      if (contractTextValue.trim().length < 20) {
        throw new Error("This contract does not contain enough readable text to extract dates and obligations.");
      }

      const response = await fetch(`${API_URL}/api/obligations/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({ contract_text: contractTextValue }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Could not extract dates and obligations.");
      }

      setObligationsResult(data);
      setObligationsMessage("Important dates and obligations extracted successfully.");
    } catch (error) {
      setObligationsMessage(error.message);
    } finally {
      setObligationsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthMessage("");
    setAuthMessageType("danger");

    if (!isLogin) {
      const password = form.password;
      const strongPassword =
        password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /\d/.test(password) &&
        /[^A-Za-z0-9]/.test(password);

      if (!strongPassword) {
        setAuthMessage(
          "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
        );
        return;
      }

      if (password !== confirmPassword) {
        setAuthMessage("Passwords do not match.");
        return;
      }
    }

    setLoading(true);

    try {
      const endpoint = isLogin
        ? `${API_URL}/api/auth/login`
        : `${API_URL}/api/auth/register`;

      const body = isLogin
        ? { email: form.email, password: form.password }
        : {
            full_name: form.full_name,
            email: form.email,
            password: form.password,
          };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
      setIsLoggedIn(true);
      setAuthMessage("");

      if (!isLogin) {
        // A new account gets its recovery code immediately after signup.
        // The user is taken to Login & Security so they can save it.
        await generateRecoveryCode();
        setActivePage("settings");
      } else {
        setActivePage("dashboard");
      }
    } catch (error) {
      setAuthMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadContracts = async () => {
    const auth = token();
    if (!auth) return [];

    try {
      const response = await fetch(`${API_URL}/api/contracts/`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not load contracts.");
      setContracts(data);
      if (!qaContractId && data.length) setQaContractId(String(data[0].id));
      return data;
    } catch (error) {
      console.error("Error loading contracts:", error);
      return [];
    }
  };

  const loadAnalysisHistory = async () => {
    const auth = token();
    if (!auth) return;

    setHistoryLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/analysis/history`, {
        headers: { Authorization: `Bearer ${auth}` },
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisHistory(Array.isArray(data.history) ? data.history : []);
        return;
      }

      // Fallback for older backend versions.
      const fallback = await Promise.all(
        contracts.map(async (contract) => {
          try {
            const itemResponse = await fetch(
              `${API_URL}/api/analysis/contract/${contract.id}`,
              { headers: { Authorization: `Bearer ${auth}` } }
            );
            if (!itemResponse.ok) return null;
            const item = await itemResponse.json();
            return {
              ...item,
              contract_title: contract.title,
              contract_type: contract.file_type,
            };
          } catch {
            return null;
          }
        })
      );

      setAnalysisHistory(
        fallback.filter(Boolean).sort((a, b) => {
          return new Date(b.created_at || 0) - new Date(a.created_at || 0);
        })
      );
    } catch (error) {
      console.error("History error:", error);
      setAnalysisHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  };

  const loadAuditLogs = async () => {
    const auth = token();
    if (!auth) return;

    setAuditLoading(true);
    setAuditError("");

    try {
      const response = await fetch(`${API_URL}/api/audit/logs?limit=100`, {
        headers: { Authorization: `Bearer ${auth}` },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Could not load activity logs.");
      }

      setAuditLogs(Array.isArray(data.logs) ? data.logs : []);
    } catch (error) {
      console.error("Audit log error:", error);
      setAuditLogs([]);
      setAuditError(error.message);
    } finally {
      setAuditLoading(false);
    }
  };

  const recordAuditEvent = async (action, contractId = null) => {
    const auth = token();
    if (!auth) return;

    try {
      await fetch(`${API_URL}/api/audit/event`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          action,
          contract_id: contractId,
        }),
      });
    } catch (error) {
      console.debug("Audit event could not be recorded:", error);
    }
  };

  useEffect(() => {
    if (!isLoggedIn) return;
    loadContracts();
  }, [isLoggedIn]);

  useEffect(() => {
    if (!isLoggedIn) return;
    loadAnalysisHistory();
  }, [isLoggedIn, contracts.length]);

  const openContract = async (contractId, shouldAudit = true) => {
    const auth = token();
    setLoadingContract(true);
    try {
      const response = await fetch(`${API_URL}/api/contracts/${contractId}`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not load contract.");
      setSelectedContract(data);
      setActivePage("contracts");
      if (shouldAudit) {
        await recordAuditEvent("Contract viewed", contractId);
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setLoadingContract(false);
    }
  };

  const createContract = async (e) => {
    e.preventDefault();
    const auth = token();
    setContractMessage("");
    setCreatingContract(true);
    resetQuestionState();
    setAnalysis(null);
    setAnalysisError("");
    setSelectedContract(null);

    try {
      const response = await fetch(`${API_URL}/api/contracts/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({ title: contractTitle, raw_text: contractText }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not create contract.");

      setContractMessage("Contract created successfully.");
      setContractTitle("");
      setContractText("");
      await loadContracts();
      setActivePage("contracts");
    } catch (error) {
      setContractMessage(error.message);
    } finally {
      setCreatingContract(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      setSelectedFile(null);
      return;
    }

    const name = file.name.toLowerCase();
    if (!name.endsWith(".pdf") && !name.endsWith(".docx")) {
      setSelectedFile(null);
      setUploadMessage("Please select a PDF or Word (.docx) file.");
      return;
    }

    setSelectedFile(file);
    setScanFile(null);
    setUploadMessage("");
    setScanMessage("");
    setUploadStage("");
  };

  const handleScanChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      setScanFile(null);
      return;
    }

    if (!file.type.startsWith("image/")) {
      setScanFile(null);
      setScanMessage("Please select a JPG, PNG, or WEBP image.");
      return;
    }

    setScanFile(file);
    setSelectedFile(null);
    setScanMessage("");
    setUploadMessage("");
    setUploadStage("");
  };

  const stopCamera = () => {
    if (cameraStreamRef.current) {
      cameraStreamRef.current.getTracks().forEach((track) => track.stop());
      cameraStreamRef.current = null;
    }

    if (cameraVideoRef.current) {
      cameraVideoRef.current.srcObject = null;
    }

    setCameraOpen(false);
  };

  const openCamera = async () => {
    setCameraError("");

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError("Camera access is not supported in this browser.");
      return;
    }

    try {
      stopCamera();
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" } },
        audio: false,
      });

      cameraStreamRef.current = stream;
      setCameraOpen(true);

      setTimeout(() => {
        if (cameraVideoRef.current) {
          cameraVideoRef.current.srcObject = stream;
        }
      }, 50);
    } catch (error) {
      if (error?.name === "NotAllowedError" || error?.name === "SecurityError") {
        setCameraError("Camera access is needed to capture a document. Click Allow in your browser permission prompt and try again.");
      } else if (error?.name === "NotFoundError") {
        setCameraError("No camera was found on this device. You can use Scan to upload a document image instead.");
      } else {
        setCameraError("Unable to open the camera. Please check browser permissions and try again.");
      }
    }
  };

  const capturePhoto = () => {
    const video = cameraVideoRef.current;

    if (!video || !video.videoWidth || !video.videoHeight) {
      setCameraError("The camera is not ready yet. Please try again.");
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (!blob) {
        setCameraError("Could not capture the camera image.");
        return;
      }

      const file = new File(
        [blob],
        `camera_scan_${Date.now()}.jpg`,
        { type: "image/jpeg" }
      );

      setScanFile(file);
      setSelectedFile(null);
      setUploadMessage("");
      setScanMessage("Photo captured successfully. Click Upload Scan to continue.");
      stopCamera();
    }, "image/jpeg", 0.92);
  };

  useEffect(() => {
    return () => {
      if (cameraStreamRef.current) {
        cameraStreamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const stopListening = () => {
    if (speechRecognitionRef.current) {
      try {
        speechRecognitionRef.current.stop();
      } catch {}
    }
    speechRecognitionRef.current = null;
    setVoiceListening(false);
  };

  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setSpeakingAnswer(false);
  };

  const resetQuestionState = ({ keepContractId = false, contractId = null } = {}) => {
    stopListening();
    stopSpeaking();
    setQuestion("");
    setQaAnswer(null);
    setQaError("");
    if (keepContractId && contractId !== null) {
      setQaContractId(String(contractId));
    } else if (!keepContractId) {
      setQaContractId("");
    }
  };

  const uploadContract = async (e) => {
    e.preventDefault();
    const auth = token();
    setUploadMessage("");
    setUploadStage("");
    setAnalysis(null);
    setAnalysisError("");
    setSelectedContract(null);
    resetQuestionState();

    if (!fileTitle.trim()) {
      setUploadMessage("Please enter a contract title.");
      return;
    }
    if (!selectedFile) {
      setUploadMessage("Please select a PDF or DOCX file.");
      return;
    }

    setUploadingFile(true);
    setUploadStage("Uploading document");
    try {
      const formData = new FormData();
      formData.append("title", fileTitle);
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/api/contracts/`, {
        method: "POST",
        headers: { Authorization: `Bearer ${auth}` },
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "File upload failed.");

      setUploadStage("Analyzing contract");
      setUploadMessage("Document uploaded. Starting analysis...");
      setFileTitle("");
      setSelectedFile(null);
      const input = document.getElementById("contractFile");
      if (input) input.value = "";
      await loadContracts();
      await analyzeContract(data.id);
    } catch (error) {
      setUploadStage("");
      setUploadMessage(error.message);
    } finally {
      setUploadingFile(false);
      setUploadStage("");
    }
  };

  const uploadScan = async (e) => {
    e.preventDefault();
    const auth = token();
    setScanMessage("");
    setUploadStage("");
    setAnalysis(null);
    setAnalysisError("");
    setSelectedContract(null);
    resetQuestionState();

    if (!fileTitle.trim()) {
      setScanMessage("Please enter a contract title.");
      return;
    }

    if (!scanFile) {
      setScanMessage("Please choose a scan image or capture one with the camera.");
      return;
    }

    setUploadingScan(true);
    setUploadStage("Uploading scan");

    try {
      setUploadStage("Extracting text");
      const formData = new FormData();
      formData.append("title", fileTitle);
      formData.append("file", scanFile);

      const response = await fetch(`${API_URL}/api/scan/upload`, {
        method: "POST",
        headers: { Authorization: `Bearer ${auth}` },
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Scan upload failed.");

      setUploadStage("Analyzing contract");
      setScanMessage("Scan processed successfully. Starting analysis...");
      setFileTitle("");
      setScanFile(null);
      const input = document.getElementById("scanFile");
      if (input) input.value = "";
      await loadContracts();
      await analyzeContract(data.id);
    } catch (error) {
      setUploadStage("");
      setScanMessage(error.message);
    } finally {
      setUploadingScan(false);
      setUploadStage("");
    }
  };

  const loadEvidenceSources = async (contractId) => {
    if (!contractId) {
      setEvidenceSources([]);
      setEvidenceError("");
      return;
    }

    const auth = token();
    setEvidenceLoading(true);
    setEvidenceError("");

    try {
      const response = await fetch(`${API_URL}/api/evidence/contract/${contractId}`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not load source evidence.");
      setEvidenceSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (error) {
      setEvidenceSources([]);
      setEvidenceError(error.message);
    } finally {
      setEvidenceLoading(false);
    }
  };

  useEffect(() => {
    if (analysis?.contract_id) {
      loadEvidenceSources(analysis.contract_id);
    } else {
      setEvidenceSources([]);
      setEvidenceError("");
    }
  }, [analysis?.contract_id]);

  const analyzeContract = async (contractId) => {
    const auth = token();
    setAnalyzingId(contractId);
    setAnalysis(null);
    setSelectedContract(null);
    setAnalysisError("");
    resetQuestionState({ keepContractId: true, contractId });

    try {
      const response = await fetch(`${API_URL}/api/analysis/${contractId}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${auth}` },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Contract analysis failed.");

      setAnalysis(data);
      await loadAnalysisHistory();
      setActivePage("analysis");
    } catch (error) {
      setAnalysisError(error.message);
    } finally {
      setAnalyzingId(null);
    }
  };

  const loadLatestAnalysis = async (contractId) => {
    const auth = token();
    setAnalysis(null);
    setAnalysisError("");
    resetQuestionState({ keepContractId: true, contractId });

    try {
      const response = await fetch(`${API_URL}/api/analysis/contract/${contractId}`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "No analysis found.");
      setAnalysis(data);
      setActivePage("analysis");
    } catch (error) {
      setAnalysisError(error.message);
    }
  };

  const askQuestion = async (e, contractIdOverride = null) => {
    if (e && typeof e.preventDefault === "function") e.preventDefault();
    const auth = token();
    const selectedQuestionContractId = contractIdOverride || qaContractId;
    setQaError("");
    setQaAnswer(null);
    stopSpeaking();
    stopListening();

    if (!selectedQuestionContractId) {
      setQaError("Please select a contract.");
      return;
    }
    if (!question.trim()) {
      setQaError("Please enter a question.");
      return;
    }

    setQaLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/qa/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth}`,
        },
        body: JSON.stringify({
          contract_id: Number(selectedQuestionContractId),
          question: question.trim(),
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Unable to answer the question.");
      setQaAnswer(data);
    } catch (error) {
      setQaError(error.message);
    } finally {
      setQaLoading(false);
    }
  };

  const downloadReport = async (contractId, format) => {
    const auth = token();
    const key = `${format}-${contractId}`;
    setReportLoading(key);
    setReportMessage("");

    try {
      const response = await fetch(`${API_URL}/api/reports/${contractId}/${format}`, {
        headers: { Authorization: `Bearer ${auth}` },
      });
      if (!response.ok) {
        let errorMessage = "Could not download the report.";
        try {
          const data = await response.json();
          errorMessage = data.detail || errorMessage;
        } catch {}
        throw new Error(errorMessage);
      }

      const blob = await response.blob();
      const extension = format === "pdf" ? "pdf" : "md";
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `contract_${contractId}_report.${extension}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setReportMessage(`${format.toUpperCase()} report downloaded successfully.`);
    } catch (error) {
      setReportMessage(error.message);
    } finally {
      setReportLoading("");
    }
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Voice input is not supported in this browser. You can type your question instead."
      );
      return;
    }

    if (voiceListening) {
      stopListening();
      return;
    }

    stopSpeaking();

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setVoiceListening(true);

    recognition.onend = () => {
      speechRecognitionRef.current = null;
      setVoiceListening(false);
    };

    recognition.onerror = () => {
      speechRecognitionRef.current = null;
      setVoiceListening(false);
    };

    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript || "";
      if (transcript.trim()) {
        setQuestion(transcript.trim());
      }
    };

    speechRecognitionRef.current = recognition;
    recognition.start();
  };

  const speakText = (textToSpeak) => {
    if (!textToSpeak || !window.speechSynthesis) {
      alert("Voice playback is not supported in this browser.");
      return;
    }

    if (speakingAnswer) {
      stopSpeaking();
      return;
    }

    stopListening();
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = "en-IN";
    utterance.rate = 0.95;
    utterance.onstart = () => setSpeakingAnswer(true);
    utterance.onend = () => setSpeakingAnswer(false);
    utterance.onerror = () => setSpeakingAnswer(false);

    setSpeakingAnswer(true);
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    return () => {
      stopListening();
      stopSpeaking();
      stopLanguageVoiceInput();
      stopLanguageSpeech();
      stopDocumentVoiceInput();
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    };
  }, []);

  const logout = () => {
    stopListening();
    stopSpeaking();
    stopLanguageVoiceInput();
    stopLanguageSpeech();
    stopDocumentVoiceInput();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setUser(null);
    setContracts([]);
    setAnalysisHistory([]);
    setSelectedContract(null);
    setAnalysis(null);
    setQuestion("");
    setQaContractId("");
    setQaAnswer(null);
    setQaError("");
    setRecoveryCode("");
    setRecoveryMessage("");
    setIsLoggedIn(false);
  };

  const stats = useMemo(() => {
    const scores = analysisHistory
      .map((item) => Number(item.overall_risk_score))
      .filter((value) => Number.isFinite(value));

    const average = scores.length
      ? Math.round(scores.reduce((sum, value) => sum + value, 0) / scores.length)
      : 0;

    const highRisk = analysisHistory.filter((item) => {
      const level = String(item.overall_risk_level || "").toLowerCase();
      return level.includes("high") || Number(item.overall_risk_score) >= 70;
    }).length;

    const mediumRisk = analysisHistory.filter((item) => {
      const level = String(item.overall_risk_level || "").toLowerCase();
      return level.includes("medium") || (Number(item.overall_risk_score) >= 40 && Number(item.overall_risk_score) < 70);
    }).length;

    const lowRisk = analysisHistory.filter((item) => {
      const level = String(item.overall_risk_level || "").toLowerCase();
      return level.includes("low") || Number(item.overall_risk_score) < 40;
    }).length;

    const coverage = contracts.length
      ? Math.round((analysisHistory.length / contracts.length) * 100)
      : 0;

    const latest = analysisHistory.length
      ? analysisHistory[0]
      : null;

    return {
      contracts: contracts.length,
      analyses: analysisHistory.length,
      average,
      highRisk,
      mediumRisk,
      lowRisk,
      coverage,
      latestTitle: latest?.contract_title || "No reviews yet",
      latestDate: latest?.created_at || null,
    };
  }, [contracts, analysisHistory]);

  if (!isLoggedIn) {
    return (
      <>
        <style>{styles}</style>
        <div className="auth-page">
          <div className="auth-glow glow-one" />
          <div className="auth-glow glow-two" />
          <div className="auth-shell">
            <section className="auth-hero">
              <div className="brand-mark large">⚖</div>
              <div className="eyebrow">AI-POWERED CONTRACT INTELLIGENCE</div>
              <h1>Understand contracts before they become problems.</h1>
              <p>
                Upload, analyze and question contracts with AI, semantic retrieval
                and a clean review workspace designed for non-legal users.
              </p>
              <div className="hero-points">
                <span>✦ Risk analysis</span>
                <span>✦ Ask questions naturally</span>
                <span>✦ Exportable reports</span>
              </div>
            </section>

            <section className="auth-card">
              <div className="brand-row">
                <div className="brand-mark">⚖</div>
                <div>
                  <strong>LegalLens AI</strong>
                  <small>Contract Risk Analyzer</small>
                </div>
              </div>

              <h2>
                {isForgotPassword
                  ? "Reset your password"
                  : isLogin
                  ? "Welcome back"
                  : "Create your workspace"}
              </h2>
              <p className="muted">
                {isForgotPassword
                  ? "Use the recovery code saved when your account was created or generated later from Login & Security."
                  : isLogin
                  ? "Sign in to continue your contract review."
                  : "Start analyzing contracts in a few clicks."}
              </p>

              {isForgotPassword ? (
                <form onSubmit={handleForgotPassword} className="stack-form">
                  <label>
                    Email
                    <input
                      type="email"
                      name="email"
                      value={form.email}
                      onChange={handleChange}
                      placeholder="you@example.com"
                      required
                    />
                  </label>

                  <label>
                    Recovery code
                    <input
                      type="text"
                      name="recovery_code"
                      value={recoveryCode}
                      onChange={(e) => setRecoveryCode(e.target.value.toUpperCase())}
                      placeholder="XXXX-XXXX-XXXX"
                      autoComplete="one-time-code"
                      inputMode="text"
                      required
                    />
                  </label>

                  <div className="recovery-note">
                    Your recovery code is created from <strong>Settings → Login &amp; Security</strong>.
                    No email is required for this reset flow.
                  </div>

                  <label>
                    New password
                    <div className="password-wrap">
                      <input
                        type={showPassword ? "text" : "password"}
                        name="password"
                        value={form.password}
                        onChange={handleChange}
                        placeholder="••••••••"
                        required
                      />
                      <button
                        type="button"
                        className="password-toggle"
                        onClick={() => setShowPassword((value) => !value)}
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        title={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? "🙈" : "👁"}
                      </button>
                    </div>
                  </label>

                  <label>
                    Confirm new password
                    <div className="password-wrap">
                      <input
                        type={showConfirmPassword ? "text" : "password"}
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Repeat your new password"
                        required
                      />
                      <button
                        type="button"
                        className="password-toggle"
                        onClick={() => setShowConfirmPassword((value) => !value)}
                        aria-label={showConfirmPassword ? "Hide confirmed password" : "Show confirmed password"}
                        title={showConfirmPassword ? "Hide password" : "Show password"}
                      >
                        {showConfirmPassword ? "🙈" : "👁"}
                      </button>
                    </div>
                  </label>

                  <div className="password-hint">
                    Use at least 8 characters with uppercase, lowercase, a number and a special character.
                  </div>

                  <button className="primary-btn full" disabled={resetLoading}>
                    {resetLoading ? "Resetting..." : "Reset password"}
                  </button>
                </form>
              ) : (
                <form onSubmit={handleSubmit} className="stack-form">
                  {!isLogin && (
                    <label>
                      Full name
                      <input name="full_name" value={form.full_name} onChange={handleChange} placeholder="Your name" required />
                    </label>
                  )}

                  <label>
                    Email
                    <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />
                  </label>

                  <label>
                    Password
                    <div className="password-wrap">
                      <input
                        type={showPassword ? "text" : "password"}
                        name="password"
                        value={form.password}
                        onChange={handleChange}
                        placeholder="••••••••"
                        required
                      />
                      <button
                        type="button"
                        className="password-toggle"
                        onClick={() => setShowPassword((value) => !value)}
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        title={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? "🙈" : "👁"}
                      </button>
                    </div>
                  </label>

                  {!isLogin && (
                    <>
                      <label>
                        Confirm password
                        <div className="password-wrap">
                          <input
                            type={showConfirmPassword ? "text" : "password"}
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Repeat your password"
                            required
                          />
                          <button
                            type="button"
                            className="password-toggle"
                            onClick={() => setShowConfirmPassword((value) => !value)}
                            aria-label={showConfirmPassword ? "Hide confirmed password" : "Show confirmed password"}
                            title={showConfirmPassword ? "Hide password" : "Show password"}
                          >
                            {showConfirmPassword ? "🙈" : "👁"}
                          </button>
                        </div>
                      </label>
                      <div className="password-hint">
                        Use at least 8 characters with uppercase, lowercase, a number and a special character.
                      </div>
                    </>
                  )}

                  {isLogin && (
                    <button
                      type="button"
                      className="forgot-link"
                      onClick={() => {
                        setIsForgotPassword(true);
                        setAuthMessage("");
                        setAuthMessageType("danger");
                        setConfirmPassword("");
                        setForm((prev) => ({ ...prev, password: "" }));
                        setShowPassword(false);
                        setShowConfirmPassword(false);
                      }}
                    >
                      Forgot password?
                    </button>
                  )}

                  <button className="primary-btn full" disabled={loading}>
                    {loading ? "Please wait..." : isLogin ? "Sign in" : "Create account"}
                  </button>
                </form>
              )}

              {authMessage && <div className={`alert ${authMessageType}`}>{authMessage}</div>}

              <div className="auth-switch">
                {isForgotPassword ? "Remembered your password?" : isLogin ? "Don't have an account?" : "Already have an account?"}
                <button
                  className="link-btn"
                  onClick={() => {
                    if (isForgotPassword) {
                      setIsForgotPassword(false);
                      setIsLogin(true);
                    } else {
                      setIsLogin(!isLogin);
                    }
                    setAuthMessage("");
                    setAuthMessageType("danger");
                    setRecoveryCode("");
                    setConfirmPassword("");
                    setForm((prev) => ({ ...prev, password: "" }));
                    setShowPassword(false);
                    setShowConfirmPassword(false);
                  }}
                >
                  {isForgotPassword ? "Back to login" : isLogin ? "Register" : "Login"}
                </button>
              </div>
            </section>
          </div>
        </div>
      </>
    );
  }

  const navItems = [
    { id: "dashboard", icon: "⌂", label: "Dashboard" },
    { id: "contracts", icon: "▤", label: "My Contracts" },
    { id: "analysis", icon: "◈", label: "Analysis" },
    { id: "document-generator", icon: "✎", label: "Document Generator" },
    { id: "clause-comparison", icon: "⇄", label: "Clause Comparison" },
    { id: "version-diff", icon: "⇆", label: "Version Diff" },
    { id: "obligations", icon: "◷", label: "Dates & Obligations" },
    { id: "language", icon: "文", label: "Multi-language" },
    { id: "history", icon: "◷", label: "Review History" },
    { id: "activity", icon: "◌", label: "Activity Log" },
    { id: "help", icon: "?", label: "Help & Guide" },
    { id: "reports", icon: "▣", label: "Reports" },
    { id: "settings", icon: "⚙", label: "Settings" },
  ];

  const pageMeta = {
    dashboard: ["Dashboard", "Your contract intelligence center"],
    contracts: ["My Contracts", "Upload, review and manage your agreements"],
    analysis: ["Analysis", "Detailed contract review, findings and recommendations"],
    "document-generator": ["Legal Document Generator", "Create a professional draft from your requirements"],
    "clause-comparison": ["Clause Comparison", "Compare two clauses and understand the important differences"],
    "version-diff": ["Contract Version Diff", "Compare two complete contract versions and see what changed"],
    obligations: ["Dates & Obligations", "Find deadlines, renewal details and concrete contract obligations"],
    language: ["Multi-language Support", "Translate contract text and explanations into supported languages"],
    history: ["Review History", "Previous contract reviews and detailed results"],
    activity: ["Activity Log", "A secure timeline of important actions in your workspace"],
    help: ["Help & Guide", "Quick answers about using LegalLens AI"],
    reports: ["Reports", "Download polished contract review reports"],
    settings: ["Settings", "Project configuration and system information"],
  };

  return (
    <>
      <style>{styles}</style>
      <div className="app-shell">
        <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
          <div className="sidebar-brand">
            <div className="brand-mark">⚖</div>
            <div>
              <strong>LegalLens AI</strong>
              <small>Risk Analyzer</small>
            </div>
          </div>

          <div className="workspace-label">WORKSPACE</div>
          <nav className="nav-list">
            {navItems.map((item) => (
              <button
                key={item.id}
                className={`nav-item ${activePage === item.id ? "active" : ""}`}
                onClick={() => {
                  setActivePage(item.id);
                  setSidebarOpen(false);
                }}
              >
                <span className="nav-icon">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
          <div className="sidebar-bottom">
            <button className="logout-link" onClick={() => setShowLogoutConfirm(true)}>↪ Sign out</button>
          </div>
        </aside>

        {sidebarOpen && <button className="sidebar-backdrop" onClick={() => setSidebarOpen(false)} />}

        <main className="main-area">
          <header className="topbar">
            <button className="mobile-menu" onClick={() => setSidebarOpen(true)}>☰</button>
            <div>
              <h2>{pageMeta[activePage][0]}</h2>
              <p>{pageMeta[activePage][1]}</p>
            </div>
            <div className="topbar-actions">
              <button className="icon-btn" onClick={() => setActivePage("help")} title="Open Help & Guide">?</button>
              <div className="user-chip">
                <div className="avatar">{(user?.full_name || "U").slice(0, 1).toUpperCase()}</div>
                <div className="user-copy">
                  <strong>{user?.full_name || "User"}</strong>
                  <small>Student workspace</small>
                </div>
              </div>
            </div>
          </header>

          <div className="content-wrap">
            {activePage === "dashboard" && (
              <DashboardPage
                user={user}
                stats={stats}
                contracts={contracts}
                analysisHistory={analysisHistory}
                historyLoading={historyLoading}
                onOpenContract={openContract}
                onOpenAnalysis={loadLatestAnalysis}
                onAnalyze={analyzeContract}
                analyzingId={analyzingId}
                setActivePage={setActivePage}
              />
            )}

            {activePage === "contracts" && (
              <ContractsPage
                contracts={contracts}
                uploadContract={uploadContract}
                fileTitle={fileTitle}
                setFileTitle={setFileTitle}
                selectedFile={selectedFile}
                handleFileChange={handleFileChange}
                uploadingFile={uploadingFile}
                uploadMessage={uploadMessage}
                uploadStage={uploadStage}
                scanFile={scanFile}
                handleScanChange={handleScanChange}
                uploadScan={uploadScan}
                uploadingScan={uploadingScan}
                scanMessage={scanMessage}
                openCamera={openCamera}
                cameraOpen={cameraOpen}
                cameraError={cameraError}
                cameraVideoRef={cameraVideoRef}
                capturePhoto={capturePhoto}
                stopCamera={stopCamera}
                createContract={createContract}
                contractTitle={contractTitle}
                setContractTitle={setContractTitle}
                contractText={contractText}
                setContractText={setContractText}
                creatingContract={creatingContract}
                contractMessage={contractMessage}
                selectedContract={selectedContract}
                openContract={openContract}
                loadingContract={loadingContract}
                analyzeContract={analyzeContract}
                analyzingId={analyzingId}
              />
            )}

            {activePage === "analysis" && (
              <AnalysisPage
                analysis={analysis}
                contracts={contracts}
                loadLatestAnalysis={loadLatestAnalysis}
                openContract={openContract}
                evidenceSources={evidenceSources}
                evidenceLoading={evidenceLoading}
                evidenceError={evidenceError}
                refreshEvidence={loadEvidenceSources}
                analysisError={analysisError}
                setActivePage={setActivePage}
                downloadReport={downloadReport}
                reportLoading={reportLoading}
                reportMessage={reportMessage}
                qaContractId={qaContractId}
                setQaContractId={setQaContractId}
                question={question}
                setQuestion={setQuestion}
                askQuestion={askQuestion}
                qaLoading={qaLoading}
                qaError={qaError}
                qaAnswer={qaAnswer}
                startListening={startListening}
                voiceListening={voiceListening}
                speakText={speakText}
                speakingAnswer={speakingAnswer}
                resetQuestionState={resetQuestionState}
              />
            )}

            {activePage === "document-generator" && (
              <DocumentGeneratorPage
                documentType={documentType}
                setDocumentType={setDocumentType}
                documentDetails={documentDetails}
                setDocumentDetails={setDocumentDetails}
                generateDocument={generateDocument}
                documentGeneratedContent={documentGeneratedContent}
                documentGeneratedSourceContent={documentGeneratedSourceContent}
                documentGenerating={documentGenerating}
                documentTranslating={documentTranslating}
                documentGeneratorMessage={documentGeneratorMessage}
                documentOutputLanguage={documentOutputLanguage}
                changeDocumentOutputLanguage={changeDocumentOutputLanguage}
                documentVoiceLanguage={documentVoiceLanguage}
                setDocumentVoiceLanguage={setDocumentVoiceLanguage}
                documentVoiceListening={documentVoiceListening}
                startDocumentVoiceInput={startDocumentVoiceInput}
                documentSpeaking={documentSpeaking}
                speakGeneratedDocument={speakGeneratedDocument}
                copyGeneratedDocument={copyGeneratedDocument}
                downloadGeneratedDocument={downloadGeneratedDocument}
                uploadDocumentReferenceFile={uploadDocumentReferenceFile}
                documentReferenceFileLoading={documentReferenceFileLoading}
                documentReferenceFileName={documentReferenceFileName}
                setDocumentDetails={setDocumentDetails}
                setDocumentReferenceFileName={setDocumentReferenceFileName}
              />
            )}

            {activePage === "clause-comparison" && (
              <ClauseComparisonPage
                clauseA={clauseA}
                setClauseA={setClauseA}
                clauseB={clauseB}
                setClauseB={setClauseB}
                clauseComparison={clauseComparison}
                clauseComparing={clauseComparing}
                clauseComparisonMessage={clauseComparisonMessage}
                compareClauses={compareClauses}
                uploadClauseFile={uploadClauseFile}
                clauseAFileLoading={clauseAFileLoading}
                clauseAFileName={clauseAFileName}
                clauseBFileLoading={clauseBFileLoading}
                clauseBFileName={clauseBFileName}
                setClauseAFileName={setClauseAFileName}
                setClauseBFileName={setClauseBFileName}
              />
            )}


            {activePage === "version-diff" && (
              <VersionDiffPage
                versionA={versionA}
                setVersionA={setVersionA}
                versionB={versionB}
                setVersionB={setVersionB}
                versionAName={versionAName}
                versionBName={versionBName}
                versionAFileLoading={versionAFileLoading}
                versionBFileLoading={versionBFileLoading}
                uploadVersionFile={uploadVersionFile}
                versionDiff={versionDiff}
                versionDiffLoading={versionDiffLoading}
                versionDiffMessage={versionDiffMessage}
                compareContractVersions={compareContractVersions}
                setVersionAName={setVersionAName}
                setVersionBName={setVersionBName}
              />
            )}

            {activePage === "obligations" && (
              <ObligationsPage
                contracts={contracts}
                obligationsContractId={obligationsContractId}
                setObligationsContractId={setObligationsContractId}
                obligationsResult={obligationsResult}
                obligationsLoading={obligationsLoading}
                obligationsMessage={obligationsMessage}
                extractObligations={extractObligations}
              />
            )}

            {activePage === "language" && (
              <LanguagePage
                languageText={languageText}
                setLanguageText={setLanguageText}
                sourceLanguage={sourceLanguage}
                setSourceLanguage={setSourceLanguage}
                targetLanguage={targetLanguage}
                setTargetLanguage={setTargetLanguage}
                translatedText={translatedText}
                translating={translating}
                translationMessage={translationMessage}
                translateText={translateText}
                copyTranslatedText={copyTranslatedText}
                uploadLanguageFile={uploadLanguageFile}
                languageFileLoading={languageFileLoading}
                languageFileName={languageFileName}
                setLanguageFileName={setLanguageFileName}
                downloadTranslatedFile={downloadTranslatedFile}
                translationDownloadLoading={translationDownloadLoading}
                languageVoiceListening={languageVoiceListening}
                startLanguageVoiceInput={startLanguageVoiceInput}
                languageSpeaking={languageSpeaking}
                speakTranslatedText={speakTranslatedText}
              />
            )}

            {activePage === "history" && (
              <ReviewHistoryPage
                contracts={contracts}
                analysisHistory={analysisHistory}
                historyLoading={historyLoading}
                loadAnalysisHistory={loadAnalysisHistory}
                loadLatestAnalysis={loadLatestAnalysis}
              />
            )}

            {activePage === "activity" && (
              <ActivityLogPage
                logs={auditLogs}
                contracts={contracts}
                loading={auditLoading}
                error={auditError}
                onRefresh={loadAuditLogs}
              />
            )}

            {activePage === "help" && <HelpPage setActivePage={setActivePage} />}

            {activePage === "reports" && (
              <ReportsPage
                contracts={contracts}
                analysisHistory={analysisHistory}
                downloadReport={downloadReport}
                reportLoading={reportLoading}
                reportMessage={reportMessage}
              />
            )}

            {activePage === "settings" && (
              <SettingsPage
                user={user}
                setAboutModal={setAboutModal}
                setShowLogoutConfirm={setShowLogoutConfirm}
                setActivePage={setActivePage}
                recoveryCode={recoveryCode}
                recoveryMessage={recoveryMessage}
                recoveryLoading={recoveryLoading}
                generateRecoveryCode={generateRecoveryCode}
                copyRecoveryCode={copyRecoveryCode}
              />
            )}
          </div>
        </main>

        {cameraOpen && (
          <div className="camera-overlay">
            <div className="camera-modal">
              <div className="camera-head">
                <div>
                  <strong>Scan with Camera</strong>
                  <small>Capture the contract page clearly and keep the camera steady.</small>
                </div>
                <button className="camera-close" onClick={stopCamera}>×</button>
              </div>

              <div className="camera-frame">
                <video
                  ref={cameraVideoRef}
                  autoPlay
                  playsInline
                  muted
                />
              </div>

              <div className="camera-actions">
                <button className="secondary-btn" onClick={stopCamera}>Cancel</button>
                <button className="primary-btn" onClick={capturePhoto}>Capture Photo</button>
              </div>
            </div>
          </div>
        )}

        <button
          className="ai-fab"
          onClick={() => setAssistantOpen(!assistantOpen)}
          title="Help & Guide"
        >
          ?
        </button>
        {assistantOpen && (
          <div className="assistant-panel">
            <div className="assistant-head">
              <div>
                <strong>Help & Guide</strong>
                <small>Quick help for using LegalLens AI</small>
              </div>
              <button onClick={() => setAssistantOpen(false)}>×</button>
            </div>

            <div className="assistant-body">
              <div className="help-grid">
                <div className="help-item">
                  <span>1</span>
                  <div>
                    <strong>Add a contract</strong>
                    <p>Use PDF, Word, Scan, Camera, or paste text.</p>
                  </div>
                </div>

                <div className="help-item">
                  <span>2</span>
                  <div>
                    <strong>Review the results</strong>
                    <p>Open Analysis to see risks, clauses and protections.</p>
                  </div>
                </div>

                <div className="help-item">
                  <span>3</span>
                  <div>
                    <strong>Ask a question</strong>
                    <p>Once a contract is analyzed, ask about that document there.</p>
                  </div>
                </div>

                <div className="help-item">
                  <span>4</span>
                  <div>
                    <strong>Download reports</strong>
                    <p>Use Reports to export the latest review.</p>
                  </div>
                </div>

                <div className="help-item">
                  <span>5</span>
                  <div>
                    <strong>Camera access</strong>
                    <p>Allow browser camera permission when you use Camera.</p>
                  </div>
                </div>

                <div className="help-item">
                  <span>6</span>
                  <div>
                    <strong>Voice help</strong>
                    <p>Use the microphone on a contract review to speak your question.</p>
                  </div>
                </div>
              </div>

              <div className="hero-actions">
                <button
                  className="secondary-btn"
                  onClick={() => {
                    setActivePage("contracts");
                    setAssistantOpen(false);
                  }}
                >
                  Add Contract
                </button>

                <button
                  className="secondary-btn"
                  onClick={() => {
                    setActivePage("help");
                    setAssistantOpen(false);
                  }}
                >
                  Open Help
                </button>
              </div>
            </div>
          </div>
        )}


        {showLogoutConfirm && (
          <div className="confirm-overlay">
            <div className="confirm-modal">
              <div className="confirm-icon">↪</div>
              <h3>Sign out?</h3>
              <p>Are you sure you want to sign out of LegalLens AI?</p>
              <div className="confirm-actions">
                <button className="secondary-btn" onClick={() => setShowLogoutConfirm(false)}>Cancel</button>
                <button className="primary-btn" onClick={() => { setShowLogoutConfirm(false); logout(); }}>Sign out</button>
              </div>
            </div>
          </div>
        )}

        {aboutModal && (
          <div className="confirm-overlay">
            <div className="about-modal">
              <div className="confirm-head">
                <div>
                  <strong>{aboutModal === "terms" ? "Terms of Use" : aboutModal === "privacy" ? "Privacy Policy" : aboutModal === "licenses" ? "Licenses" : "Report a Bug"}</strong>
                  <small>LegalLens AI</small>
                </div>
                <button className="camera-close" onClick={() => setAboutModal("")}>×</button>
              </div>
              <div className="about-modal-body">
                {aboutModal === "terms" && <p>LegalLens AI is provided as a project application for contract review and document analysis. Use the results as informational assistance and review important decisions independently.</p>}
                {aboutModal === "privacy" && <p>This project stores account and contract information needed to provide its features. Keep sensitive documents limited to appropriate test or authorized use, and do not upload information you are not permitted to process.</p>}
                {aboutModal === "licenses" && <p>This project uses third-party open-source packages and services, including React, FastAPI, PostgreSQL, Groq, Sentence Transformers, FAISS, EasyOCR and related dependencies. Their respective licenses apply to those components.</p>}
                {aboutModal === "bug" && (
                  <div>
                    <p>Describe the issue and include the page where it happened.</p>
                    <button className="primary-btn" onClick={() => { window.location.href = "mailto:?subject=LegalLens AI Bug Report&body=Page:%20%5Benter%20page%5D%0AProblem:%20%5Bdescribe%20the%20issue%5D%0ASteps:%20%5Bwhat%20you%20did%5D"; }}>Open email to report</button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

function DashboardPage({ user, stats, contracts, analysisHistory, historyLoading, onOpenContract, onOpenAnalysis, onAnalyze, analyzingId, setActivePage }) {
  const recentContracts = contracts.slice(-5).reverse();
  const recentAnalyses = analysisHistory.slice(0, 5);

  return (
    <div className="page-stack">
      <section className="hero-banner">
        <div className="hero-content">
          <div className="eyebrow">AI CONTRACT REVIEW WORKSPACE</div>
          <h1>Hello, {user?.full_name?.split(" ")[0] || "there"}. Ready to review?</h1>
          <p>Analyze contract language, surface risk signals, retrieve relevant clauses and create shareable reports from one workspace.</p>
          <div className="hero-actions">
            <button className="primary-btn" onClick={() => setActivePage("contracts")}>+ Add Contract</button>
            <button className="ghost-btn light" onClick={() => setActivePage("analysis")}>View Analysis</button>
          </div>
        </div>
        <div className="hero-orb"><span>✦</span></div>
      </section>

      <section className="stats-grid">
        <MetricCard label="Total Contracts" value={stats.contracts} icon="▤" note="Documents in workspace" />
        <MetricCard label="Completed Analyses" value={stats.analyses} icon="◈" note="Latest result per contract" />
        <MetricCard label="Average Risk" value={`${stats.average}/100`} icon="◎" note="Across analyzed contracts" />
        <MetricCard label="High-Risk Contracts" value={stats.highRisk} icon="!" note="Requires closer review" accent="danger" />
      </section>

      <section className="dashboard-grid two-col">
        <div className="panel">
          <div className="panel-head">
            <div><h3>Recent Contracts</h3><p>Your latest uploaded or created agreements.</p></div>
            <button className="text-btn" onClick={() => setActivePage("contracts")}>View all →</button>
          </div>
          <div className="contract-list compact">
            {recentContracts.length === 0 ? <EmptyState text="No contracts yet." /> : recentContracts.map((contract) => (
              <div className="list-row" key={contract.id}>
                <div className="row-icon doc">▤</div>
                <div className="row-main"><strong>{contract.title}</strong><small>{friendlyFileType(contract.file_type)} • {formatDate(contract.created_at)}</small></div>
                <button className="mini-btn" onClick={() => onOpenContract(contract.id)}>Open</button>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <div><h3>Latest Analyses</h3><p>One current analysis is shown per contract.</p></div>
            <button className="text-btn" onClick={() => setActivePage("history")}>Open history →</button>
          </div>
          <div className="analysis-list compact">
            {historyLoading ? <EmptyState text="Loading analysis history..." /> : recentAnalyses.length === 0 ? <EmptyState text="No completed analyses yet." /> : recentAnalyses.map((item) => (
              <div className="list-row" key={item.id}>
                <div className="row-icon analysis">◈</div>
                <div className="row-main"><strong>{item.contract_title}</strong><small>{formatDate(item.created_at)}</small></div>
                <div className="score-badge">
                  <strong>{item.overall_risk_score}</strong>
                  <RiskPill level={item.overall_risk_level} />
                </div>
                <button className="mini-btn" onClick={() => onOpenAnalysis(item.contract_id)}>View</button>
              </div>
            ))}
          </div>
        </div>
      </section>


      <section className="dashboard-grid two-col">
        <div className="panel help-card">
          <div className="panel-head">
            <div><h3>How to use the app</h3><p>You can complete a contract review in a few simple steps.</p></div>
          </div>
          <div className="help-grid">
            <div className="help-item"><span>1</span><div><strong>Upload</strong><p>Add a PDF, Word file, scanned page, or camera photo.</p></div></div>
            <div className="help-item"><span>2</span><div><strong>Review</strong><p>Let the AI summarize the document and highlight areas to review.</p></div></div>
            <div className="help-item"><span>3</span><div><strong>Ask</strong><p>Type or speak a question about the document.</p></div></div>
            <div className="help-item"><span>4</span><div><strong>Report</strong><p>Download a PDF or Markdown report when you are finished.</p></div></div>
          </div>
        </div>

        <div className="panel help-card">
          <div className="panel-head">
            <div><h3>What the analyzer checks</h3><p>The review focuses on information found in the uploaded document.</p></div>
          </div>
          <div className="check-list">
            <div>✓ Risk signals and unusual terms</div>
            <div>✓ Important or potentially risky clauses</div>
            <div>✓ Missing standard protections</div>
            <div>✓ Plain-language explanations and recommendations</div>
            <div>✓ Questions answered from the document content</div>
          </div>
        </div>
      </section>

      <section className="panel workflow-panel">
        <div className="panel-head"><div><h3>How LegalLens AI works</h3><p>A simple four-step workflow from document to useful review.</p></div></div>
        <div className="workflow">
          <WorkflowStep n="01" title="Upload" text="PDF, Word, Scan or Camera" />
          <WorkflowStep n="02" title="Understand" text="Find the relevant parts of your document" />
          <WorkflowStep n="03" title="Analyze" text="Identify risks, clauses and missing protections" />
          <WorkflowStep n="04" title="Ask & Report" text="Ask questions and download your report" />
        </div>
      </section>
    </div>
  );
}

function ContractsPage({ contracts, uploadContract, fileTitle, setFileTitle, selectedFile, handleFileChange, uploadingFile, uploadMessage, uploadStage, scanFile, handleScanChange, uploadScan, uploadingScan, scanMessage, openCamera, cameraOpen, cameraError, cameraVideoRef, capturePhoto, stopCamera, createContract, contractTitle, setContractTitle, contractText, setContractText, creatingContract, contractMessage, selectedContract, openContract, loadingContract, analyzeContract, analyzingId }) {
  const [contractSearch, setContractSearch] = useState("");
  const [contractTypeFilter, setContractTypeFilter] = useState("all");
  const [contractSort, setContractSort] = useState("newest");

  const filteredContracts = [...contracts]
    .filter((contract) => {
      const query = contractSearch.trim().toLowerCase();
      if (!query) return true;
      return `${contract.title || ""} ${contract.file_name || ""}`.toLowerCase().includes(query);
    })
    .filter((contract) => {
      if (contractTypeFilter === "all") return true;
      return friendlyFileType(contract.file_type).toLowerCase() === contractTypeFilter;
    })
    .sort((a, b) => {
      const aTime = a.created_at ? new Date(a.created_at).getTime() : 0;
      const bTime = b.created_at ? new Date(b.created_at).getTime() : 0;

      // The current contracts API does not return created_at for these records.
      // Fall back to the database id so newest/oldest still works reliably.
      const aOrder = Number.isFinite(aTime) && aTime > 0 ? aTime : Number(a.id) || 0;
      const bOrder = Number.isFinite(bTime) && bTime > 0 ? bTime : Number(b.id) || 0;

      return contractSort === "oldest" ? aOrder - bOrder : bOrder - aOrder;
    });

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div><h1>Contract workspace</h1><p>Keep agreements, uploads and extracted text organized in one place.</p></div>
        <div className="pill neutral">{contracts.length} contracts</div>
      </section>

      <section className="dashboard-grid two-col">
        <div className="panel upload-panel">
          <div className="section-icon purple">↑</div>
          <h3>Add a contract</h3>
          <p className="muted">Choose PDF, Word, Scan, or Camera.</p>

          <form
            onSubmit={scanFile ? uploadScan : uploadContract}
            className="stack-form"
          >
            <label>
              Contract title
              <input
                value={fileTitle}
                onChange={(e) => setFileTitle(e.target.value)}
                placeholder="e.g. Vendor Agreement"
              />
            </label>

            <div className="upload-options">
              <button
                type="button"
                className="upload-option"
                onClick={() => document.getElementById("contractFile")?.click()}
              >
                <span>▤</span>
                <strong>PDF</strong>
                <small>Upload PDF</small>
              </button>

              <button
                type="button"
                className="upload-option"
                onClick={() => document.getElementById("contractFile")?.click()}
              >
                <span>W</span>
                <strong>Word</strong>
                <small>Upload DOCX</small>
              </button>

              <button
                type="button"
                className="upload-option"
                onClick={() => document.getElementById("scanFile")?.click()}
              >
                <span>▧</span>
                <strong>Scan</strong>
                <small>Upload image</small>
              </button>

              <button
                type="button"
                className="upload-option"
                onClick={openCamera}
              >
                <span>◉</span>
                <strong>Camera</strong>
                <small>Capture page</small>
              </button>
            </div>

            <input
              id="contractFile"
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              className="hidden-file-input"
            />

            <input
              id="scanFile"
              type="file"
              accept="image/*"
              onChange={handleScanChange}
              className="hidden-file-input"
            />

            {selectedFile && (
              <div className="file-chip">▤ {selectedFile.name}</div>
            )}

            {scanFile && (
              <div className="file-chip scan-chip">▧ {scanFile.name}</div>
            )}

            <button
              className="primary-btn"
              disabled={uploadingFile || uploadingScan}
            >
              {uploadingFile
                ? "Uploading..."
                : uploadingScan
                ? "Processing..."
                : scanFile
                ? "Upload Scan"
                : "Upload Contract"}
            </button>

            {uploadStage && (
              <div className="upload-progress" aria-live="polite">
                <div className="upload-progress-line">
                  <span className="progress-dot active" />
                  <span>
                    {uploadStage}
                  </span>
                </div>
                <div className="progress-track">
                  <span
                    className="progress-fill"
                    style={{
                      width:
                        uploadStage === "Uploading document" || uploadStage === "Uploading scan"
                          ? "38%"
                          : uploadStage === "Extracting text"
                          ? "62%"
                          : "86%",
                    }}
                  />
                </div>
              </div>
            )}
          </form>

          {uploadMessage && (
            <div className={`alert ${uploadMessage.toLowerCase().includes("success") ? "success" : "danger"}`}>
              {uploadMessage}
            </div>
          )}

          {scanMessage && (
            <div className={`alert ${scanMessage.toLowerCase().includes("success") || scanMessage.toLowerCase().includes("captured") ? "success" : "danger"}`}>
              {scanMessage}
            </div>
          )}

          {cameraError && <div className="alert danger">{cameraError}</div>}
        </div>

        <div className="panel upload-panel">
          <div className="section-icon blue">✎</div>
          <h3>Create from text</h3>
          <p className="muted">Paste a contract when you do not have a file.</p>
          <form onSubmit={createContract} className="stack-form">
            <label>Contract title<input value={contractTitle} onChange={(e) => setContractTitle(e.target.value)} placeholder="e.g. Employment Agreement" /></label>
            <label>Contract text<textarea rows="7" value={contractText} onChange={(e) => setContractText(e.target.value)} placeholder="Paste contract text here..." /></label>
            <button className="secondary-btn" disabled={creatingContract}>{creatingContract ? "Creating..." : "Create Contract"}</button>
          </form>
          {contractMessage && <div className={`alert ${contractMessage.toLowerCase().includes("success") ? "success" : "danger"}`}>{contractMessage}</div>}
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div><h3>My Contracts</h3><p>Search, filter, sort and manage your agreements.</p></div>
          <div className="pill neutral">{filteredContracts.length} shown</div>
        </div>

        <div className="contract-toolbar" style={{ display: "grid", gridTemplateColumns: "minmax(220px, 1.6fr) minmax(150px, .8fr) minmax(150px, .8fr)", gap: "10px", marginBottom: "16px" }}>
          <input
            value={contractSearch}
            onChange={(e) => setContractSearch(e.target.value)}
            placeholder="Search by contract name or file name"
            aria-label="Search contracts"
            style={{ width: "100%" }}
          />
          <select value={contractTypeFilter} onChange={(e) => setContractTypeFilter(e.target.value)} aria-label="Filter contracts by type">
            <option value="all">All file types</option>
            <option value="pdf">PDF</option>
            <option value="word">Word</option>
            <option value="scan">Scan</option>
            <option value="camera">Camera</option>
            <option value="text">Text</option>
          </select>
          <select value={contractSort} onChange={(e) => setContractSort(e.target.value)} aria-label="Sort contracts">
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
          </select>
        </div>

        {contracts.length === 0 ? <EmptyState text="No contracts found." /> : filteredContracts.length === 0 ? (
          <EmptyState text="No contracts match your search or filter." />
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead><tr><th>Contract</th><th>Type</th><th>Added</th><th>Actions</th></tr></thead>
              <tbody>
                {filteredContracts.map((contract) => (
                  <tr key={contract.id}>
                    <td><div className="table-title"><span className="row-icon doc">▤</span><div><strong>{contract.title}</strong><small>{contract.file_name || "Text contract"}</small></div></div></td>
                    <td><span className="pill neutral">{friendlyFileType(contract.file_type)}</span></td>
                    <td>{formatDate(contract.created_at)}</td>
                    <td><div className="table-actions"><button className="mini-btn" onClick={() => openContract(contract.id)}>{loadingContract ? "Loading..." : "View"}</button><button className="mini-btn primary-mini" onClick={() => analyzeContract(contract.id)} disabled={analyzingId === contract.id}>{analyzingId === contract.id ? "Analyzing..." : "Analyze"}</button></div></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {selectedContract && (
        <section className="panel details-panel">
          <div className="panel-head"><div><h3>{selectedContract.title}</h3><p>Extracted document text and source details.</p></div><button className="mini-btn" onClick={() => openContract(selectedContract.id, false)}>Refresh</button></div>
          <div className="contract-meta-grid">
            <div><span>File name</span><strong>{selectedContract.file_name || "Text Contract"}</strong></div>
            <div><span>File type</span><strong>{selectedContract.file_type}</strong></div>
            <div><span>Created</span><strong>{formatDate(selectedContract.created_at)}</strong></div>
          </div>
          <div className="document-viewer">{selectedContract.raw_text || "No contract text available."}</div>
        </section>
      )}
    </div>
  );
}

function AnalysisPage({
  analysis,
  contracts,
  loadLatestAnalysis,
  openContract,
  evidenceSources,
  evidenceLoading,
  evidenceError,
  refreshEvidence,
  analysisError,
  setActivePage,
  downloadReport,
  reportLoading,
  reportMessage,
  qaContractId,
  setQaContractId,
  question,
  setQuestion,
  askQuestion,
  qaLoading,
  qaError,
  qaAnswer,
  startListening,
  voiceListening,
  speakText,
  speakingAnswer,
  resetQuestionState,
}) {
  const contract = analysis
    ? contracts.find((item) => item.id === analysis.contract_id)
    : null;

  const flaggedClauses = analysis
    ? normalizeArray(analysis.flagged_clauses)
    : [];
  const missingProtections = analysis
    ? normalizeArray(analysis.missing_standard_protections)
    : [];
  const recommendations = analysis
    ? normalizeArray(analysis.recommendations)
    : [];
  const categoryRisks = analysis
    ? normalizeArray(analysis.category_risks)
    : [];

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Contract analysis</h1>
          <p>Detailed review of risk, clauses, protections and recommendations.</p>
        </div>
      </section>

      {analysisError && <div className="alert danger">{analysisError}</div>}

      {!analysis ? (
        <section className="empty-analysis">
          <div className="empty-icon">◈</div>
          <h3>No contract analysis selected</h3>
          <p>Upload a contract from My Contracts or open a previous review from Review History.</p>
          <div className="hero-actions">
            <button className="primary-btn" onClick={() => setActivePage("contracts")}>Go to My Contracts</button>
            <button className="secondary-btn" onClick={() => setActivePage("history")}>Open Review History</button>
          </div>
        </section>
      ) : (
        <>
          <section className="analysis-hero-panel">
            <div className="analysis-hero-main">
              <span className="eyebrow">LATEST REVIEW</span>
              <h2>{contract?.title || "Current document"}</h2>
              <p>{friendlyFileType(contract?.file_type)} • {formatDate(analysis.created_at)}</p>
            </div>
            <div className="risk-score-card">
              <span>Overall risk score</span>
              <strong>{analysis.overall_risk_score}/100</strong>
              <RiskPill level={analysis.overall_risk_level} large />
            </div>
          </section>

          <section className="stats-grid">
            <MetricCard
              label="Risk score"
              value={`${analysis.overall_risk_score}/100`}
              icon="◎"
              note={analysis.overall_risk_level || "Overall assessment"}
              accent={String(analysis.overall_risk_level || "").toLowerCase().includes("high") ? "danger" : ""}
            />
            <MetricCard
              label="Flagged clauses"
              value={flaggedClauses.length}
              icon="!"
              note="Clauses needing review"
            />
            <MetricCard
              label="Missing protections"
              value={missingProtections.length}
              icon="△"
              note="Protections not identified"
            />
            <MetricCard
              label="Recommendations"
              value={recommendations.length}
              icon="✓"
              note="Review suggestions"
            />
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Summary</h3>
                <p>Plain-language overview of the current document review.</p>
              </div>
            </div>
            <p className="long-text">{analysis.summary || "No summary available."}</p>
          </section>

          <section className="panel category-risk-panel">
            <div className="panel-head">
              <div>
                <h3>Category risks</h3>
                <p>Risk levels across the main review categories.</p>
              </div>
            </div>
            <CategoryRiskSection categories={analysis.category_risks} />
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Missing protections</h3>
                <p>Standard protections that were not identified in the document.</p>
              </div>
            </div>
            <div className="chip-list">
              {missingProtections.length ? missingProtections.map((item, index) => (
                <div className="insight-card" key={index}>
                  <strong>{item.protection || item.title || "Missing protection"}</strong>
                  <p>{item.reason || item.description || "No explanation available."}</p>
                  <RiskPill level={item.importance} />
                </div>
              )) : <EmptyState text="No missing protections reported." />}
            </div>
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Flagged clauses</h3>
                <p>Clauses that may deserve closer review.</p>
              </div>
            </div>
            <FlaggedClauses clauses={analysis.flagged_clauses} />
          </section>

          <EvidenceSourcesPanel
            sources={evidenceSources}
            loading={evidenceLoading}
            error={evidenceError}
            onOpenDocument={async () => { await recordAuditEvent("Source evidence viewed", analysis.contract_id); await openContract(analysis.contract_id, false); }}
            onRefresh={() => refreshEvidence(analysis.contract_id)}
          />

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Recommendations</h3>
                <p>Practical review suggestions based on the document analysis.</p>
              </div>
            </div>
            <Recommendations items={analysis.recommendations} />
          </section>

          <section className="panel contract-help-panel">
            <div className="panel-head">
              <div>
                <h3>Questions about this document</h3>
                <p>Ask something about the contract you are currently reviewing.</p>
              </div>
              <span className="pill purple-pill">Document Q&amp;A</span>
            </div>

            <form onSubmit={askQuestion} className="stack-form">
              <textarea
                rows="4"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Example: What are the payment terms in this document?"
              />

              <div className="question-tools">
                <button
                  className={`voice-btn ${voiceListening ? "listening" : ""}`}
                  type="button"
                  onClick={startListening}
                >
                  {voiceListening ? "⏹ Stop listening" : "🎙 Speak question"}
                </button>
                <span className="muted-small">Voice input or typing is available.</span>
              </div>

              <div className="hero-actions">
                <button className="primary-btn" type="submit" disabled={qaLoading}>
                  {qaLoading ? "Finding answer..." : "Ask about this document"}
                </button>

                {question && (
                  <button
                    className="secondary-btn"
                    type="button"
                    onClick={() =>
                      resetQuestionState({
                        keepContractId: true,
                        contractId: qaContractId,
                      })
                    }
                  >
                    Clear
                  </button>
                )}
              </div>
            </form>

            {qaError && <div className="alert danger">{qaError}</div>}

            {qaAnswer && (
              <div className="answer-box contract-answer-box">
                <div className="answer-toolbar">
                  <strong>Answer</strong>
                  <button
                    className="voice-btn small"
                    type="button"
                    onClick={() => speakText(qaAnswer.answer_text)}
                  >
                    {speakingAnswer ? "⏹ Stop" : "🔊 Listen"}
                  </button>
                </div>
                <p>{qaAnswer.answer_text}</p>
              </div>
            )}
          </section>

          <section className="scoreboard-panel">
            <div className="scoreboard-header">
              <div>
                <span className="eyebrow scoreboard-eyebrow">REVIEW SCOREBOARD</span>
                <h3>Contract review scorecard</h3>
                <p>A final at-a-glance view of the current review.</p>
              </div>
              <div className="scoreboard-total">
                <span>Overall score</span>
                <strong>{analysis.overall_risk_score}/100</strong>
                <RiskPill level={analysis.overall_risk_level} large />
              </div>
            </div>

            <div className="scoreboard-grid">
              <div className="scoreboard-item">
                <span>Risk categories</span>
                <strong>{categoryRisks.length}</strong>
                <small>Reviewed areas</small>
              </div>
              <div className="scoreboard-item">
                <span>Flagged clauses</span>
                <strong>{flaggedClauses.length}</strong>
                <small>Need closer review</small>
              </div>
              <div className="scoreboard-item">
                <span>Missing protections</span>
                <strong>{missingProtections.length}</strong>
                <small>Not identified</small>
              </div>
              <div className="scoreboard-item">
                <span>Recommendations</span>
                <strong>{recommendations.length}</strong>
                <small>Review suggestions</small>
              </div>
            </div>
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Export report</h3>
                <p>Download the current review for your presentation or records.</p>
              </div>
            </div>
            <div className="hero-actions">
              <button
                className="primary-btn"
                onClick={() => downloadReport(analysis.contract_id, "pdf")}
                disabled={reportLoading === `pdf-${analysis.contract_id}`}
              >
                {reportLoading === `pdf-${analysis.contract_id}` ? "Preparing..." : "Download PDF"}
              </button>
              <button
                className="secondary-btn"
                onClick={() => downloadReport(analysis.contract_id, "markdown")}
                disabled={reportLoading === `markdown-${analysis.contract_id}`}
              >
                {reportLoading === `markdown-${analysis.contract_id}` ? "Preparing..." : "Download Markdown"}
              </button>
            </div>
            {reportMessage && <div className="alert success">{reportMessage}</div>}
          </section>
        </>
      )}
    </div>
  );
}

function DocumentGeneratorPage({
  documentType,
  setDocumentType,
  documentDetails,
  setDocumentDetails,
  generateDocument,
  documentGeneratedContent,
  documentGeneratedSourceContent,
  documentGenerating,
  documentTranslating,
  documentGeneratorMessage,
  documentOutputLanguage,
  changeDocumentOutputLanguage,
  documentVoiceLanguage,
  setDocumentVoiceLanguage,
  documentVoiceListening,
  startDocumentVoiceInput,
  documentSpeaking,
  speakGeneratedDocument,
  copyGeneratedDocument,
  downloadGeneratedDocument,
  uploadDocumentReferenceFile,
  documentReferenceFileLoading,
  documentReferenceFileName,
  setDocumentReferenceFileName,
}) {
  const documentTypes = [
    "Non-Disclosure Agreement",
    "Employment Agreement",
    "Freelance Agreement",
    "Service Agreement",
    "Lease Agreement",
    "Internship Agreement",
    "Partnership Agreement",
    "Business Proposal",
    "Other",
  ];

  const languages = SUPPORTED_LANGUAGES;

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Legal Document Generator</h1>
          <p>Create a professional first draft from the details you provide.</p>
        </div>
      </section>

      <section className="dashboard-grid two-col document-generator-grid">
        <div className="panel">
          <div className="section-icon purple">✎</div>
          <h3>Create a document</h3>
          <p className="muted">Choose the document type and describe what you need included.</p>

          <form onSubmit={generateDocument} className="stack-form">
            <label>
              Document type
              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
              >
                {documentTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </label>

            <div>
              <div className="language-source-head">
                <strong>Reference document or requirements</strong>
                <label className="upload-document-btn">
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                    onChange={uploadDocumentReferenceFile}
                  />
                  {documentReferenceFileLoading ? "Reading document..." : "Upload PDF / Word / TXT"}
                </label>
              </div>
              {documentReferenceFileName && (
                <div className="language-file-chip">
                  <span>📄 {documentReferenceFileName}</span>
                  <button
                    type="button"
                    onClick={() => {
                      setDocumentDetails("");
                      setDocumentReferenceFileName("");
                    }}
                  >
                    Clear
                  </button>
                </div>
              )}
              <div className="question-tools">
                <label style={{ margin: 0, flex: 1 }}>
                  Document language
                  <select
                    value={documentOutputLanguage}
                    onChange={(e) => changeDocumentOutputLanguage(e.target.value)}
                    disabled={documentTranslating}
                  >
                    {languages.map((lang) => (
                      <option key={`document-${lang}`} value={lang}>{lang}</option>
                    ))}
                  </select>
                </label>
                <label style={{ margin: 0, flex: 1 }}>
                  Voice language
                  <select
                    value={documentVoiceLanguage}
                    onChange={(e) => setDocumentVoiceLanguage(e.target.value)}
                  >
                    {languages.map((language) => (
                      <option key={language} value={language}>{language}</option>
                    ))}
                  </select>
                </label>
                <button
                  className={`voice-btn ${documentVoiceListening ? "listening" : ""}`}
                  type="button"
                  onClick={startDocumentVoiceInput}
                >
                  {documentVoiceListening ? "⏹ Stop" : "🎙 Speak"}
                </button>
              </div>
              <textarea
                rows="12"
                value={documentDetails}
                onChange={(e) => {
                  setDocumentDetails(e.target.value);
                  if (e.target.value !== documentDetails) setDocumentReferenceFileName("");
                }}
                placeholder="Upload a reference document, or describe what the new document should contain..."
              />
              <p className="language-file-help">Upload an existing PDF, Word or TXT file to use its text as the starting requirements, or enter the requirements manually.</p>
            </div>

            <button className="primary-btn" type="submit" disabled={documentGenerating || documentTranslating}>
              {documentGenerating ? "Generating document..." : documentTranslating ? "Translating document..." : "Generate Document"}
            </button>
          </form>

          {documentGeneratorMessage && (
            <div className={`alert ${documentGeneratorMessage.toLowerCase().includes("success") || documentGeneratorMessage.toLowerCase().includes("copied") || documentGeneratorMessage.toLowerCase().includes("downloaded") ? "success" : "danger"}`}>
              {documentGeneratorMessage}
            </div>
          )}

          <div className="generator-note">
            <strong>Use generated drafts as a starting point.</strong>
            <span>Review important details and adapt the draft before using it for a real situation.</span>
          </div>
        </div>

        <div className="panel document-output-panel">
          <div className="panel-head">
            <div>
              <h3>Generated document</h3>
              <p>Your draft will appear here.</p>
            </div>
            {documentGeneratedContent && (
              <div className="table-actions">
                <button className="mini-btn" type="button" onClick={speakGeneratedDocument}>
                  {documentSpeaking ? "⏹ Stop" : "🔊 Listen"}
                </button>
                <button className="mini-btn" type="button" onClick={copyGeneratedDocument}>Copy</button>
                <button className="mini-btn primary-mini" type="button" onClick={downloadGeneratedDocument}>Download PDF</button>
              </div>
            )}
          </div>

          {documentGeneratedContent ? (
            <pre className="generated-document">{documentGeneratedContent}</pre>
          ) : (
            <div className="generator-empty">
              <div className="empty-icon">✎</div>
              <h3>No document generated yet</h3>
              <p>Complete the form on the left and generate your first draft.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function ClauseComparisonPage({
  clauseA,
  setClauseA,
  clauseB,
  setClauseB,
  clauseComparison,
  clauseComparing,
  clauseComparisonMessage,
  compareClauses,
  uploadClauseFile,
  clauseAFileLoading,
  clauseAFileName,
  clauseBFileLoading,
  clauseBFileName,
  setClauseAFileName,
  setClauseBFileName,
}) {
  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Clause Comparison</h1>
          <p>Compare two contract clauses and understand the important changes in simple language.</p>
        </div>
      </section>

      <section className="dashboard-grid two-col">
        <div className="panel">
          <div className="section-icon purple">A</div>
          <div className="language-source-head">
            <div>
              <h3>Clause A</h3>
              <p className="muted">Upload a document or paste the first clause.</p>
            </div>
            <label className="upload-document-btn">
              <input
                type="file"
                accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                onChange={(e) => uploadClauseFile(e, "A")}
              />
              {clauseAFileLoading ? "Reading..." : "Upload file"}
            </label>
          </div>
          {clauseAFileName && (
            <div className="language-file-chip">
              <span>📄 {clauseAFileName}</span>
              <button type="button" onClick={() => { setClauseA(""); setClauseAFileName(""); }}>Clear</button>
            </div>
          )}
          <textarea
            rows="14"
            value={clauseA}
            onChange={(e) => {
              setClauseA(e.target.value);
              if (e.target.value !== clauseA) setClauseAFileName("");
            }}
            placeholder="Upload a PDF/Word/TXT file, or paste Clause A here..."
          />
          <p className="language-file-help">After uploading, review and edit the extracted text so only the clause you want to compare remains.</p>
        </div>

        <div className="panel">
          <div className="section-icon blue">B</div>
          <div className="language-source-head">
            <div>
              <h3>Clause B</h3>
              <p className="muted">Upload a document or paste the second clause.</p>
            </div>
            <label className="upload-document-btn">
              <input
                type="file"
                accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                onChange={(e) => uploadClauseFile(e, "B")}
              />
              {clauseBFileLoading ? "Reading..." : "Upload file"}
            </label>
          </div>
          {clauseBFileName && (
            <div className="language-file-chip">
              <span>📄 {clauseBFileName}</span>
              <button type="button" onClick={() => { setClauseB(""); setClauseBFileName(""); }}>Clear</button>
            </div>
          )}
          <textarea
            rows="14"
            value={clauseB}
            onChange={(e) => {
              setClauseB(e.target.value);
              if (e.target.value !== clauseB) setClauseBFileName("");
            }}
            placeholder="Upload a PDF/Word/TXT file, or paste Clause B here..."
          />
          <p className="language-file-help">After uploading, review and edit the extracted text so only the clause you want to compare remains.</p>
        </div>
      </section>

      <section className="panel">
        <div className="hero-actions">
          <button
            className="primary-btn"
            type="button"
            onClick={compareClauses}
            disabled={clauseComparing}
          >
            {clauseComparing ? "Comparing clauses..." : "Compare Clauses"}
          </button>
        </div>

        {clauseComparisonMessage && (
          <div
            className={`alert ${clauseComparisonMessage.toLowerCase().includes("success") ? "success" : "danger"}`}
          >
            {clauseComparisonMessage}
          </div>
        )}
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Comparison Result</h3>
            <p>Important differences and review points from the two clauses.</p>
          </div>
        </div>

        {clauseComparison ? (
          <pre className="generated-document">{clauseComparison}</pre>
        ) : (
          <div className="generator-empty">
            <div className="empty-icon">⇄</div>
            <h3>No comparison yet</h3>
            <p>Paste two clauses above and compare them to see the result here.</p>
          </div>
        )}
      </section>

      <div className="generator-note">
        <strong>Comparison is based only on the text you provide.</strong>
        <span>Review important wording and decisions independently before using the result in a real legal situation.</span>
      </div>
    </div>
  );
}


function VersionDiffPage({
  versionA,
  setVersionA,
  versionB,
  setVersionB,
  versionAName,
  versionBName,
  versionAFileLoading,
  versionBFileLoading,
  uploadVersionFile,
  versionDiff,
  versionDiffLoading,
  versionDiffMessage,
  compareContractVersions,
  setVersionAName,
  setVersionBName,
}) {
  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Contract Version Diff</h1>
          <p>Upload two versions of a contract and identify added, removed and modified terms.</p>
        </div>
      </section>

      <section className="dashboard-grid two-col">
        <div className="panel">
          <div className="section-icon purple">1</div>
          <div className="language-source-head">
            <div>
              <h3>Version 1</h3>
              <p className="muted">Upload PDF, Word or TXT, or paste the first version.</p>
            </div>
            <label className="upload-document-btn">
              <input
                type="file"
                accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                onChange={(e) => uploadVersionFile(e, "A")}
              />
              {versionAFileLoading ? "Reading..." : "Upload file"}
            </label>
          </div>
          {versionAName && (
            <div className="language-file-chip">
              <span>📄 {versionAName}</span>
              <button type="button" onClick={() => { setVersionA(""); setVersionAName(""); }}>Clear</button>
            </div>
          )}
          <textarea
            rows="15"
            value={versionA}
            onChange={(e) => {
              setVersionA(e.target.value);
              setVersionAName("");
            }}
            placeholder="Paste Version 1 here, or upload a document..."
          />
        </div>

        <div className="panel">
          <div className="section-icon blue">2</div>
          <div className="language-source-head">
            <div>
              <h3>Version 2</h3>
              <p className="muted">Upload the revised contract or paste the second version.</p>
            </div>
            <label className="upload-document-btn">
              <input
                type="file"
                accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                onChange={(e) => uploadVersionFile(e, "B")}
              />
              {versionBFileLoading ? "Reading..." : "Upload file"}
            </label>
          </div>
          {versionBName && (
            <div className="language-file-chip">
              <span>📄 {versionBName}</span>
              <button type="button" onClick={() => { setVersionB(""); setVersionBName(""); }}>Clear</button>
            </div>
          )}
          <textarea
            rows="15"
            value={versionB}
            onChange={(e) => {
              setVersionB(e.target.value);
              setVersionBName("");
            }}
            placeholder="Paste Version 2 here, or upload a document..."
          />
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Compare contract versions</h3>
            <p>The AI compares the supplied text and reports the important changes.</p>
          </div>
          <button className="primary-btn" onClick={compareContractVersions} disabled={versionDiffLoading}>
            {versionDiffLoading ? "Comparing versions..." : "Compare Versions"}
          </button>
        </div>
        {versionDiffMessage && (
          <div className={`alert ${versionDiffMessage.toLowerCase().includes("successfully") || versionDiffMessage.toLowerCase().includes("loaded") ? "success" : "danger"}`}>
            {versionDiffMessage}
          </div>
        )}
      </section>

      {versionDiff ? (
        <>
          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Overall change summary</h3>
                <p>{versionAName || "Version 1"} → {versionBName || "Version 2"}</p>
              </div>
            </div>
            <p className="long-text">{versionDiff.overall_summary}</p>
          </section>

          <section className="dashboard-grid two-col">
            <div className="panel">
              <h3>Key changes</h3>
              {versionDiff.key_changes?.length ? (
                <div className="check-list">
                  {versionDiff.key_changes.map((item, index) => <div key={index}>✓ {item}</div>)}
                </div>
              ) : <EmptyState text="No key changes reported." />}
            </div>
            <div className="panel">
              <h3>Dates &amp; amounts changed</h3>
              {versionDiff.dates_amounts_changed?.length ? (
                <div className="check-list">
                  {versionDiff.dates_amounts_changed.map((item, index) => <div key={index}>• {item}</div>)}
                </div>
              ) : <EmptyState text="No date or amount changes reported." />}
            </div>
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <h3>Detailed changes</h3>
                <p>Added, removed and modified contract language identified by the comparison.</p>
              </div>
            </div>
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Section</th>
                    <th>Change</th>
                    <th>Version 1</th>
                    <th>Version 2</th>
                    <th>Practical impact</th>
                  </tr>
                </thead>
                <tbody>
                  {versionDiff.changes?.length ? versionDiff.changes.map((change, index) => (
                    <tr key={index}>
                      <td><strong>{change.section}</strong></td>
                      <td><span className="pill neutral">{change.change_type}</span></td>
                      <td><div className="long-cell">{change.version_a}</div></td>
                      <td><div className="long-cell">{change.version_b}</div></td>
                      <td><div className="long-cell">{change.impact}</div></td>
                    </tr>
                  )) : (
                    <tr><td colSpan="5"><EmptyState text="No material changes were identified." /></td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel">
            <h3>Points to review</h3>
            {versionDiff.review_points?.length ? (
              <div className="check-list">
                {versionDiff.review_points.map((item, index) => <div key={index}>→ {item}</div>)}
              </div>
            ) : <EmptyState text="No additional review points reported." />}
          </section>
        </>
      ) : (
        <section className="panel">
          <div className="generator-empty">
            <div className="empty-icon">⇆</div>
            <h3>No version comparison yet</h3>
            <p>Upload or paste two versions of the same contract, then compare them.</p>
          </div>
        </section>
      )}

      <div className="generator-note">
        <strong>Comparison is based only on the two documents you provide.</strong>
        <span>Review important wording independently before using the result in a real legal situation.</span>
      </div>
    </div>
  );
}

function ObligationsPage({
  contracts,
  obligationsContractId,
  setObligationsContractId,
  obligationsResult,
  obligationsLoading,
  obligationsMessage,
  extractObligations,
}) {
  const selected = contracts.find((contract) => String(contract.id) === String(obligationsContractId));

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Dates &amp; Obligations</h1>
          <p>Detect important dates, deadlines, renewal details and concrete obligations from a contract.</p>
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Select a contract</h3>
            <p>The selected contract is loaded from your LegalLens AI workspace.</p>
          </div>
          <button className="primary-btn" onClick={extractObligations} disabled={obligationsLoading || !contracts.length}>
            {obligationsLoading ? "Extracting..." : "Find Dates & Obligations"}
          </button>
        </div>

        <select value={obligationsContractId} onChange={(e) => { setObligationsContractId(e.target.value); }}>
          <option value="">Select a contract</option>
          {contracts.map((contract) => (
            <option key={contract.id} value={contract.id}>
              {contract.title}
            </option>
          ))}
        </select>

        {selected && (
          <div className="language-file-chip" style={{ marginTop: 14 }}>
            <span>📄 {selected.title}</span>
            <span className="muted">{friendlyFileType(selected.file_type)}</span>
          </div>
        )}

        {!contracts.length && <EmptyState text="Add a contract first from My Contracts." />}

        {obligationsMessage && (
          <div className={`alert ${obligationsMessage.toLowerCase().includes("successfully") ? "success" : "danger"}`}>
            {obligationsMessage}
          </div>
        )}
      </section>

      {obligationsResult && (
        <>
          <section className="dashboard-grid two-col">
            <div className="panel">
              <div className="panel-head">
                <div>
                  <h3>Important dates</h3>
                  <p>Dates and time periods identified from the contract.</p>
                </div>
              </div>
              {obligationsResult.important_dates?.length ? (
                <div className="insight-list">
                  {obligationsResult.important_dates.map((item, index) => (
                    <div className="insight-card" key={index}>
                      <strong>{item.label}</strong>
                      <p><b>{item.value}</b></p>
                      {item.source && <small>{item.source}</small>}
                      {item.notes && <p>{item.notes}</p>}
                    </div>
                  ))}
                </div>
              ) : <EmptyState text="No important dates were identified." />}
            </div>

            <div className="panel">
              <div className="panel-head">
                <div>
                  <h3>Contract obligations</h3>
                  <p>Concrete responsibilities and deadlines found in the document.</p>
                </div>
              </div>
              {obligationsResult.obligations?.length ? (
                <div className="insight-list">
                  {obligationsResult.obligations.map((item, index) => (
                    <div className="insight-card" key={index}>
                      <div className="row-between"><strong>{item.obligation_type}</strong><span className="pill neutral">{item.deadline}</span></div>
                      <p>{item.requirement}</p>
                      <p><strong>Responsible party:</strong> {item.responsible_party}</p>
                      {item.source && <small>{item.source}</small>}
                      {item.notes && <p>{item.notes}</p>}
                    </div>
                  ))}
                </div>
              ) : <EmptyState text="No concrete obligations were identified." />}
            </div>
          </section>

          <section className="dashboard-grid two-col">
            <div className="panel">
              <h3>Renewal alerts</h3>
              {obligationsResult.renewal_alerts?.length ? (
                <div className="check-list">
                  {obligationsResult.renewal_alerts.map((item, index) => <div key={index}>→ {item}</div>)}
                </div>
              ) : <EmptyState text="No renewal alerts were identified." />}
            </div>
            <div className="panel">
              <h3>Notes</h3>
              {obligationsResult.general_notes?.length ? (
                <div className="check-list">
                  {obligationsResult.general_notes.map((item, index) => <div key={index}>• {item}</div>)}
                </div>
              ) : <EmptyState text="No additional notes." />}
            </div>
          </section>

          <div className="generator-note">
            <strong>Results are extracted only from the selected contract.</strong>
            <span>Review the original wording before relying on any date, deadline or obligation.</span>
          </div>
        </>
      )}
    </div>
  );
}

function LanguagePage({
  languageText,
  setLanguageText,
  sourceLanguage,
  setSourceLanguage,
  targetLanguage,
  setTargetLanguage,
  translatedText,
  translating,
  translationMessage,
  translateText,
  copyTranslatedText,
  uploadLanguageFile,
  languageFileLoading,
  languageFileName,
  setLanguageFileName,
  downloadTranslatedFile,
  translationDownloadLoading,
  languageVoiceListening,
  startLanguageVoiceInput,
  languageSpeaking,
  speakTranslatedText,
}) {
  const languages = SUPPORTED_LANGUAGES;

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Multi-language Support</h1>
          <p>Translate contract text, explanations and other project content into a supported language.</p>
        </div>
      </section>

      <section className="dashboard-grid two-col">
        <div className="panel">
          <div className="section-icon purple">文</div>
          <h3>Text to translate</h3>
          <p className="muted">Paste a contract clause, explanation or other text.</p>

          <form onSubmit={translateText} className="stack-form">
            <label>
              Source language
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
              >
                {languages.map((language) => (
                  <option key={language} value={language}>{language}</option>
                ))}
              </select>
            </label>

            <label>
              Target language
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
              >
                {languages.map((language) => (
                  <option key={language} value={language}>{language}</option>
                ))}
              </select>
            </label>

            <div>
              <div className="language-source-head">
                <strong>Source document or text</strong>
                <label className="upload-document-btn">
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                    onChange={uploadLanguageFile}
                  />
                  {languageFileLoading ? "Reading document..." : "Upload PDF / Word / TXT"}
                </label>
              </div>
              {languageFileName && (
                <div className="language-file-chip">
                  <span>📄 {languageFileName}</span>
                  <button
                    type="button"
                    onClick={() => {
                      setLanguageText("");
                    }}
                  >
                    Clear
                  </button>
                </div>
              )}
              <div className="question-tools">
                <button
                  className={`voice-btn ${languageVoiceListening ? "listening" : ""}`}
                  type="button"
                  onClick={startLanguageVoiceInput}
                >
                  {languageVoiceListening ? "⏹ Stop listening" : "🎙 Speak text"}
                </button>
                <span className="muted-small">Speak in the selected source language or type normally.</span>
              </div>
              <textarea
                rows="12"
                value={languageText}
                onChange={(e) => {
                  setLanguageText(e.target.value);
                  if (e.target.value !== languageText) setLanguageFileName("");
                }}
                placeholder="Upload a PDF/Word/TXT file, or paste text here..."
              />
              <p className="language-file-help">PDF and Word files are converted into text automatically, so you do not need to type the whole contract.</p>
            </div>

            <button className="primary-btn" type="submit" disabled={translating}>
              {translating ? "Translating..." : "Translate Text"}
            </button>
          </form>

          {translationMessage && (
            <div className={`alert ${translationMessage.toLowerCase().includes("success") || translationMessage.toLowerCase().includes("copied") ? "success" : "danger"}`}>
              {translationMessage}
            </div>
          )}
        </div>

        <div className="panel">
          <div className="panel-head">
            <div>
              <h3>Translated result</h3>
              <p>Your translated text will appear here.</p>
            </div>
            {translatedText && (
              <div className="translation-actions">
                <button className="mini-btn" type="button" onClick={speakTranslatedText}>
                  {languageSpeaking ? "⏹ Stop" : "🔊 Listen"}
                </button>
                <button className="mini-btn" type="button" onClick={copyTranslatedText}>
                  Copy
                </button>
                <button
                  className="mini-btn primary-mini"
                  type="button"
                  onClick={() => downloadTranslatedFile("pdf")}
                  disabled={!!translationDownloadLoading}
                >
                  {translationDownloadLoading === "pdf" ? "Preparing PDF..." : "Download PDF"}
                </button>
                <button
                  className="mini-btn primary-mini"
                  type="button"
                  onClick={() => downloadTranslatedFile("docx")}
                  disabled={!!translationDownloadLoading}
                >
                  {translationDownloadLoading === "docx" ? "Preparing Word..." : "Download Word"}
                </button>
              </div>
            )}
          </div>

          {translatedText ? (
            <div className="generated-document">
              {translatedText}
            </div>
          ) : (
            <div className="generator-empty">
              <div className="empty-icon">文</div>
              <h3>No translation yet</h3>
              <p>Enter text and choose a target language to translate it.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function ReviewHistoryPage({ contracts, analysisHistory, historyLoading, loadAnalysisHistory, loadLatestAnalysis }) {
  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Review history</h1>
          <p>One latest review is shown for each contract. Open any review to see its full analysis.</p>
        </div>
        <button className="secondary-btn" onClick={loadAnalysisHistory} disabled={historyLoading}>
          {historyLoading ? "Refreshing..." : "Refresh history"}
        </button>
      </section>

      <section className="stats-grid">
        <MetricCard label="Reviewed Contracts" value={analysisHistory.length} icon="◷" note="One latest record per contract" />
        <MetricCard label="High Risk" value={analysisHistory.filter((item) => String(item.overall_risk_level || "").toLowerCase().includes("high") || Number(item.overall_risk_score) >= 70).length} icon="!" note="High-risk reviews" accent="danger" />
        <MetricCard label="Medium Risk" value={analysisHistory.filter((item) => String(item.overall_risk_level || "").toLowerCase().includes("medium") || (Number(item.overall_risk_score) >= 40 && Number(item.overall_risk_score) < 70)).length} icon="△" note="Medium-risk reviews" />
        <MetricCard label="Low Risk" value={analysisHistory.filter((item) => String(item.overall_risk_level || "").toLowerCase().includes("low") || Number(item.overall_risk_score) < 40).length} icon="✓" note="Low-risk reviews" />
      </section>

      <section className="panel">
        <div className="table-wrap">
          <table className="data-table">
            <thead><tr><th>Contract</th><th>Risk</th><th>Score</th><th>Reviewed</th><th></th></tr></thead>
            <tbody>
              {analysisHistory.length === 0 ? (
                <tr><td colSpan="5"><EmptyState text="No completed reviews found." /></td></tr>
              ) : analysisHistory.map((item) => (
                <tr key={item.contract_id}>
                  <td><strong>{item.contract_title}</strong><small>{friendlyFileType(contracts.find((c) => c.id === item.contract_id)?.file_type)} • {formatDate(item.created_at)}</small></td>
                  <td><RiskPill level={item.overall_risk_level} /></td>
                  <td><strong className="table-score">{item.overall_risk_score}</strong><span className="muted-small">/100</span></td>
                  <td>{formatDate(item.created_at)}</td>
                  <td><button className="mini-btn" onClick={() => loadLatestAnalysis(item.contract_id)}>View review</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function RiskDistributionRow({ label, count, total, tone }) {
  const width = Math.round((count / total) * 100);
  return (
    <div className="risk-row">
      <div className="risk-row-top"><span>{label}</span><strong>{count}</strong></div>
      <div className="risk-track"><span className={tone} style={{ width: `${width}%` }} /></div>
    </div>
  );
}

function ActivityLogPage({ logs, contracts, loading, error, onRefresh }) {
  const contractNames = useMemo(() => {
    return new Map(contracts.map((contract) => [Number(contract.id), contract.title]));
  }, [contracts]);

  const actionLabel = (action) => {
    const value = String(action || "");
    if (value.includes("POST /api/contracts")) return "Contract action";
    if (value.includes("GET /api/contracts")) return "Contract viewed";
    if (value.includes("/analysis")) return "Contract analysis";
    if (value.includes("/qa")) return "Contract Q&A";
    if (value.includes("/reports")) return "Report activity";
    if (value.includes("/version-diff")) return "Version comparison";
    if (value.includes("/obligations")) return "Dates & obligations";
    if (value.includes("/evidence-sources")) return "Source evidence";
    if (value.includes("/language")) return "Language support";
    if (value.includes("/document-generator")) return "Document generation";
    if (value.includes("/clause-comparison")) return "Clause comparison";
    if (value.includes("/scan")) return "Document scan";
    return value || "Application activity";
  };

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Activity Log</h1>
          <p>Review a chronological record of important actions performed in your workspace.</p>
        </div>
        <button className="secondary-btn" onClick={onRefresh} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh activity"}
        </button>
      </section>

      {error && <div className="alert danger">{error}</div>}

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Recent activity</h3>
            <p>Only activity associated with your authenticated account is shown.</p>
          </div>
          <div className="pill neutral">{logs.length} events</div>
        </div>

        {loading ? (
          <EmptyState text="Loading activity..." />
        ) : logs.length === 0 ? (
          <EmptyState text="No activity has been recorded yet." />
        ) : (
          <div className="activity-list">
            {logs.map((log) => {
              const contractName = log.contract_id
                ? contractNames.get(Number(log.contract_id)) || `Contract #${log.contract_id}`
                : "Workspace";
              const success = Number(log.status_code) >= 200 && Number(log.status_code) < 400;

              return (
                <div className="activity-row" key={log.id}>
                  <div className="activity-icon">◌</div>
                  <div className="activity-main">
                    <div className="activity-top">
                      <strong>{actionLabel(log.action)}</strong>
                      <span className={`activity-status ${success ? "ok" : "problem"}`}>
                        {log.status_code}
                      </span>
                    </div>
                    <p>{contractName}</p>
                    <small>{log.method === "UI" ? "User action" : `${log.method} · ${log.path}`}</small>
                  </div>
                  <time>{formatDate(log.created_at)}</time>
                </div>
              );
            })}
          </div>
        )}
      </section>

      <div className="disclaimer">
        Activity logs are intended for security and traceability. They do not contain passwords,
        recovery codes, or the full contents of uploaded contracts.
      </div>
    </div>
  );
}

function HelpPage({ setActivePage }) {
  const helpItems = [
    {
      title: "How do I add a contract?",
      text: "Go to My Contracts and choose PDF, Word, Scan, Camera, or paste the contract text.",
    },
    {
      title: "What happens after upload?",
      text: "The document is extracted, analyzed, and the latest review opens on the Analysis page.",
    },
    {
      title: "Where do I ask questions?",
      text: "Open an analyzed contract. The question-and-answer box appears on that contract's Analysis page.",
    },
    {
      title: "Where are previous reviews?",
      text: "Use Review History to see the latest saved review for each contract.",
    },
    {
      title: "How do I export a report?",
      text: "Open a completed analysis and use the Export report section to download PDF or Markdown.",
    },
    {
      title: "Can I use my voice?",
      text: "Use Speak question when a microphone is available. Use Stop listening to end voice capture.",
    },
  ];

  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Help &amp; Guide</h1>
          <p>Quick answers for common questions about using LegalLens AI.</p>
        </div>
      </section>

      <section className="panel help-card">
        <div className="help-grid help-grid-three">
          {helpItems.map((item, index) => (
            <div className="help-item" key={index}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{item.title}</strong>
                <p>{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Quick actions</h3>
            <p>Jump directly to the part of the application you need.</p>
          </div>
        </div>
        <div className="hero-actions">
          <button className="primary-btn" onClick={() => setActivePage("contracts")}>Add Contract</button>
          <button className="secondary-btn" onClick={() => setActivePage("analysis")}>Open Analysis</button>
          <button className="secondary-btn" onClick={() => setActivePage("history")}>Review History</button>
          <button className="secondary-btn" onClick={() => setActivePage("reports")}>Reports</button>
        </div>
      </section>
    </div>
  );
}

function QaPage({ contracts, qaContractId, setQaContractId, question, setQuestion, askQuestion, qaLoading, qaError, qaAnswer, startListening, voiceListening, speakText, speakingAnswer, resetQuestionState }) {
  const prompts = [
    "What are the payment terms?",
    "What termination rights are mentioned?",
    "Who owns the intellectual property?",
  ];

  return (
    <div className="page-stack">
      <section className="section-intro"><div><h1>Contract Q&A</h1><p>Ask natural-language questions and get answers grounded in the selected document.</p></div></section>
      <section className="qa-layout">
        <div className="panel qa-compose">
          <div className="section-icon blue">◇</div>
          <h3>Ask the contract</h3>
          <p className="muted">Choose a document, then type or speak your question.</p>
          <label>
            Contract
            <select
              value={qaContractId}
              onChange={(e) => {
                const nextId = e.target.value;
                if (nextId) {
                  resetQuestionState({ keepContractId: true, contractId: nextId });
                } else {
                  resetQuestionState();
                }
              }}
            >
              <option value="">Select a contract</option>
              {contracts.map((contract) => (
                <option key={contract.id} value={contract.id}>
                  {contract.title}
                </option>
              ))}
            </select>
          </label>
          <label>Question<textarea rows="5" value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask something about the contract..." /></label>
          <div className="prompt-chips">{prompts.map((prompt) => <button key={prompt} onClick={() => setQuestion(prompt)}>{prompt}</button>)}</div>
          <div className="question-tools">
            <button className={`voice-btn ${voiceListening ? "listening" : ""}`} type="button" onClick={startListening}>
              {voiceListening ? "⏹ Stop listening" : "🎙 Speak question"}
            </button>
            <span className="muted-small">Use your microphone or type normally.</span>
          </div>
          <button className="primary-btn full" onClick={askQuestion} disabled={qaLoading}>{qaLoading ? "Finding answer..." : "Ask Question"}</button>
          {qaError && <div className="alert danger">{qaError}</div>}
        </div>

        <div className="panel answer-panel">
          <div className="panel-head"><div><h3>Answer</h3><p>Response based on the selected document</p></div><span className="pill purple-pill">AI answer</span></div>
          {!qaAnswer ? <EmptyState text="Your answer will appear here after you ask a question." /> : (
            <>
              <div className="answer-box"><div className="answer-toolbar"><strong>AI answer</strong><button className="voice-btn small" type="button" onClick={() => speakText(qaAnswer.answer_text)}>{speakingAnswer ? "⏹ Stop" : "🔊 Listen"}</button></div><p>{qaAnswer.answer_text}</p></div>
            </>
          )}
        </div>
      </section>
    </div>
  );
}

function ReportsPage({ contracts, analysisHistory, downloadReport, reportLoading, reportMessage }) {
  return (
    <div className="page-stack">
      <section className="section-intro"><div><h1>Reports</h1><p>Generate clean PDF and Markdown reports from your latest contract analyses.</p></div></section>
      {reportMessage && <div className="alert success">{reportMessage}</div>}
      <section className="panel">
        <div className="table-wrap">
          <table className="data-table">
            <thead><tr><th>Contract</th><th>Risk</th><th>Last analysis</th><th>Exports</th></tr></thead>
            <tbody>
              {contracts.map((contract) => {
                const item = analysisHistory.find((analysis) => analysis.contract_id === contract.id);
                return (
                  <tr key={contract.id}>
                    <td><strong>{contract.title}</strong><small>{friendlyFileType(contract.file_type)} • {formatDate(contract.created_at)}</small></td>
                    <td>{item ? <><strong className="table-score">{item.overall_risk_score}</strong><span className="muted-small">/100</span> <RiskPill level={item.overall_risk_level} /></> : <span className="muted-small">Not analyzed</span>}</td>
                    <td>{item ? formatDate(item.created_at) : "—"}</td>
                    <td><div className="table-actions"><button className="mini-btn primary-mini" disabled={!item || reportLoading === `pdf-${contract.id}`} onClick={() => downloadReport(contract.id, "pdf")}>PDF</button><button className="mini-btn" disabled={!item || reportLoading === `markdown-${contract.id}`} onClick={() => downloadReport(contract.id, "markdown")}>MD</button></div></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function SettingsPage({
  user,
  setAboutModal,
  setShowLogoutConfirm,
  setActivePage,
  recoveryCode,
  recoveryMessage,
  recoveryLoading,
  generateRecoveryCode,
  copyRecoveryCode,
}) {
  return (
    <div className="page-stack">
      <section className="section-intro">
        <div>
          <h1>Settings</h1>
          <p>Manage your account, security and application information.</p>
        </div>
      </section>

      <section className="panel settings-card">
        <div className="setting-icon">◉</div>
        <h3>Account</h3>
        <div className="setting-row"><span>Name</span><strong>{user?.full_name || "User"}</strong></div>
        <div className="setting-row"><span>Email</span><strong>{user?.email || "—"}</strong></div>
      </section>

      <section className="panel settings-card">
        <div className="setting-icon">⌾</div>
        <h3>Login &amp; Security</h3>
        <p className="muted">Manage your sign-in session and prepare a secure password recovery option.</p>
        <div className="setting-row"><span>Sign-in method</span><strong>Email &amp; password</strong></div>
        <div className="setting-row"><span>Password</span><strong>Protected</strong></div>
        <div className="setting-row"><span>Current session</span><strong>Active</strong></div>

        <div className="recovery-box">
          <div>
            <strong>Recovery code</strong>
            <p>
              Generate a recovery code now and save it somewhere private. You can use it from
              <strong> Forgot password?</strong> without email verification.
            </p>
          </div>

          {recoveryCode ? (
            <div className="recovery-code-row">
              <code>{recoveryCode}</code>
              <button className="mini-btn" onClick={copyRecoveryCode}>Copy</button>
            </div>
          ) : (
            <div className="recovery-empty">No recovery code displayed.</div>
          )}

          <button className="secondary-btn" onClick={generateRecoveryCode} disabled={recoveryLoading}>
            {recoveryLoading ? "Generating..." : recoveryCode ? "Generate new code" : "Generate recovery code"}
          </button>

          {recoveryMessage && (
            <div className={`alert ${recoveryMessage.toLowerCase().includes("could not") ? "danger" : "success"}`}>
              {recoveryMessage}
            </div>
          )}
        </div>

        <div className="hero-actions">
          <button className="secondary-btn" onClick={() => setShowLogoutConfirm(true)}>Sign out</button>
        </div>
      </section>

      <section className="panel settings-card">
        <div className="setting-icon">ⓘ</div>
        <h3>About</h3>
        <p className="muted">Help, product information and project policies.</p>
        <div className="about-list">
          <button className="about-row" onClick={() => setActivePage("help")}><span>Help Center</span><strong>›</strong></button>
          <button className="about-row" onClick={() => setAboutModal("terms")}><span>Terms of Use</span><strong>›</strong></button>
          <button className="about-row" onClick={() => setAboutModal("privacy")}><span>Privacy Policy</span><strong>›</strong></button>
          <button className="about-row" onClick={() => setAboutModal("licenses")}><span>Licenses</span><strong>›</strong></button>
          <button className="about-row" onClick={() => setAboutModal("bug")}><span>Report a Bug</span><strong>›</strong></button>
        </div>
      </section>
    </div>
  );
}

function MetricCard({ label, value, icon, note, accent }) {
  return <div className={`metric-card ${accent || ""}`}><div className="metric-top"><div className="metric-icon">{icon}</div><span>{label}</span></div><strong>{value}</strong><small>{note}</small></div>;
}

function WorkflowStep({ n, title, text }) {
  return <div className="workflow-step"><span>{n}</span><div><strong>{title}</strong><small>{text}</small></div></div>;
}

function RiskPill({ level, large }) {
  const normalized = String(level || "Unknown").toLowerCase();
  let tone = "neutral-risk";
  if (normalized.includes("high")) tone = "high-risk";
  else if (normalized.includes("medium") || normalized.includes("moderate")) tone = "medium-risk";
  else if (normalized.includes("low")) tone = "low-risk";
  return <span className={`risk-pill ${tone} ${large ? "large" : ""}`}>{level || "Unknown"}</span>;
}

function CategoryRiskSection({ categories }) {
  const values = normalizeArray(categories);
  if (!values.length) return <EmptyState text="No category risk details available." />;
  return <div className="category-risk-grid">{values.map((item, index) => <div className="category-card" key={index}><div className="category-head"><strong>{item.category || item.name || "Category"}</strong><RiskPill level={item.risk_level} /></div><div className="category-meter"><span style={{ width: `${Math.min(100, Number(item.risk_score || 0))}%` }} /></div><p>{item.explanation || item.summary || item.description || "No explanation available."}</p><small>Risk score: {item.risk_score ?? "—"}/100</small></div>)}</div>;
}

function FlaggedClauses({ clauses }) {
  const values = normalizeArray(clauses);
  if (!values.length) return <EmptyState text="No flagged clauses reported." />;
  return <div className="clause-list">{values.map((item, index) => <div className="clause-card" key={item.id || index}><div className="category-head"><strong>{item.category || "Flagged clause"}</strong><RiskPill level={item.severity} /></div><div className="clause-section"><span>Original clause</span><blockquote>{item.original_snippet || item.snippet || "No clause text available."}</blockquote></div><div className="clause-section"><span>Issue</span><p>{item.issue_summary || item.issue || "No issue summary available."}</p></div><div className="revision-box"><span>Suggested revision</span><p>{item.suggested_revision || "No suggested revision available."}</p></div></div>)}</div>;
}

function EvidenceSourcesPanel({ sources, loading, error, onOpenDocument, onRefresh }) {
  return (
    <section className="panel">
      <div className="panel-head">
        <div>
          <h3>Source evidence</h3>
          <p>See where each flagged clause appears in the uploaded document.</p>
        </div>
        <div className="hero-actions compact-actions">
          <button className="secondary-btn" type="button" onClick={onRefresh} disabled={loading}>
            {loading ? "Finding sources..." : "Refresh sources"}
          </button>
          {sources.length > 0 && (
            <button className="mini-btn primary-mini" type="button" onClick={onOpenDocument}>
              Open document
            </button>
          )}
        </div>
      </div>

      {error && <div className="alert danger">{error}</div>}

      {loading ? (
        <EmptyState text="Locating flagged clauses in the document..." />
      ) : !sources.length ? (
        <EmptyState text="No source evidence is available for this analysis." />
      ) : (
        <div className="evidence-list">
          {sources.map((item, index) => {
            const source = item.source || {};
            return (
              <div className="evidence-card" key={item.clause_id || index}>
                <div className="category-head">
                  <div>
                    <strong>{item.category || `Flagged clause ${index + 1}`}</strong>
                    <small className="evidence-meta">
                      {source.section || "Section not detected"} · {source.line_number ? `Line ${source.line_number}` : "Line not detected"}
                    </small>
                  </div>
                  <RiskPill level={item.severity} />
                </div>

                <div className="evidence-source-box">
                  <span>Matched clause</span>
                  <blockquote>{source.clause_text || item.original_snippet || "No matching text found."}</blockquote>
                </div>
                {source.context && (
                  <div className="evidence-context-box">
                    <span>Document context</span>
                    <blockquote>{source.context}</blockquote>
                  </div>
                )}

                {source.matched ? (
                  <div className="evidence-meta-row">
                    <span>✓ Matched in uploaded contract</span>
                    <span>Characters {source.start_char}–{source.end_char}</span>
                  </div>
                ) : (
                  <div className="evidence-meta-row warning">
                    <span>⚠ Exact source text could not be located</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

function Recommendations({ items }) {
  const values = normalizeArray(items);
  if (!values.length) return <EmptyState text="No recommendations available." />;
  return <div className="recommendation-grid">{values.map((item, index) => <div className="recommendation-card" key={item.id || index}><div className="recommendation-number">{String(index + 1).padStart(2, "0")}</div><div><strong>{item.title || `Recommendation ${index + 1}`}</strong><p>{item.description || "No description available."}</p><RiskPill level={item.importance} /></div></div>)}</div>;
}

function HealthItem({ label, value }) {
  return <div className="health-item"><span>{label}</span><strong><i className="status-dot" /> {value}</strong></div>;
}

function EmptyState({ text }) { return <div className="empty-state"><div className="empty-dot">·</div><span>{text}</span></div>; }

function friendlyFileType(type) {
  const normalized = String(type || "text").toLowerCase();
  if (normalized === "pdf" || normalized.includes("pdf")) return "PDF";
  if (normalized === "docx" || normalized.includes("word")) return "Word";
  if (normalized === "scan" || normalized.includes("image")) return "Scan";
  if (normalized === "camera") return "Camera";
  return "Text";
}

function normalizeArray(value) {
  if (Array.isArray(value)) return value;
  if (typeof value === "string") {
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
  return [];
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString([], { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

const styles = `
:root{--navy:#101a3b;--navy-2:#172554;--indigo:#5b5cf0;--blue:#2563eb;--purple:#7c5cff;--cyan:#24b7d7;--bg:#f6f8fc;--panel:#fff;--border:#e7eaf2;--text:#111827;--muted:#64748b;--soft:#f3f5fb;--green:#15803d;--green-bg:#eaf8ef;--amber:#b45309;--amber-bg:#fff6df;--red:#b91c1c;--red-bg:#fff0f0;--shadow:0 12px 35px rgba(31,41,55,.06)}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--text);background:var(--bg)}button,input,textarea,select{font:inherit}button{cursor:pointer}.app-shell{min-height:100vh;background:var(--bg)}.sidebar{position:fixed;left:0;top:0;bottom:0;width:245px;background:#fff;border-right:1px solid var(--border);padding:22px 16px;display:flex;flex-direction:column;z-index:30;overflow-y:auto;overflow-x:hidden;scrollbar-width:thin;scrollbar-color:#cbd5e1 transparent}.sidebar-brand,.brand-row{display:flex;align-items:center;gap:12px}.brand-mark{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--indigo),var(--cyan));color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 8px 18px rgba(91,92,240,.22)}.brand-mark.large{width:56px;height:56px;border-radius:18px;font-size:26px;margin-bottom:22px}.sidebar-brand strong,.brand-row strong{display:block;font-size:15px;color:var(--navy)}.sidebar-brand small,.brand-row small{display:block;color:#94a3b8;margin-top:2px;font-size:11px}.workspace-label{font-size:10px;letter-spacing:.14em;color:#94a3b8;font-weight:800;margin:32px 10px 10px}.nav-list{display:flex;flex-direction:column;gap:5px}.nav-item{border:0;background:transparent;color:#64748b;text-align:left;padding:11px 12px;border-radius:10px;display:flex;align-items:center;gap:12px;font-weight:600}.nav-item:hover{background:#f4f5ff;color:var(--indigo)}.nav-item.active{background:linear-gradient(90deg,#eef0ff,#f6f2ff);color:var(--indigo);box-shadow:inset 3px 0 0 var(--indigo)}.nav-icon{width:20px;text-align:center}.sidebar-bottom{margin-top:auto}.sidebar-info{display:flex;align-items:center;gap:10px;padding:12px;background:#f8fafc;border:1px solid var(--border);border-radius:12px}.sidebar-info strong{font-size:12px;display:block}.sidebar-info small{font-size:10px;color:#94a3b8}.status-dot{width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;box-shadow:0 0 0 4px #dcfce7}.logout-link{margin-top:10px;width:100%;background:transparent;border:0;color:#64748b;text-align:left;padding:9px 8px;font-weight:600}.main-area{margin-left:245px;min-height:100vh}.topbar{height:82px;background:#fff;border-bottom:1px solid var(--border);padding:0 34px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:20}.topbar h2{margin:0;color:var(--navy);font-size:18px}.topbar p{margin:4px 0 0;color:#94a3b8;font-size:12px}.topbar-actions{display:flex;align-items:center;gap:12px}.icon-btn,.mobile-menu{border:1px solid var(--border);background:#fff;border-radius:10px;width:38px;height:38px;color:var(--indigo)}.mobile-menu{display:none}.user-chip{display:flex;align-items:center;gap:9px;padding:7px 10px;border:1px solid var(--border);border-radius:12px;background:#fff}.avatar{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,var(--indigo),var(--cyan));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px}.user-copy strong{display:block;font-size:12px}.user-copy small{display:block;color:#94a3b8;font-size:10px}.content-wrap{max-width:1320px;margin:0 auto;padding:30px}.page-stack{display:flex;flex-direction:column;gap:22px}.hero-banner{background:linear-gradient(120deg,#111a3f 0%,#24356d 58%,#4338ca 100%);border-radius:22px;padding:36px 38px;color:#fff;display:flex;align-items:center;justify-content:space-between;overflow:hidden;position:relative;box-shadow:0 20px 45px rgba(17,24,39,.15)}.hero-banner:after{content:"";position:absolute;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(72,220,255,.25),transparent 65%);right:-90px;top:-80px}.hero-content{max-width:760px;position:relative;z-index:2}.eyebrow{font-size:10px;letter-spacing:.16em;font-weight:800;opacity:.72}.hero-banner h1{font-size:34px;line-height:1.1;margin:10px 0 12px}.hero-banner p{max-width:700px;color:#dbe7ff;line-height:1.7;margin:0}.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}.hero-orb{width:160px;height:160px;border-radius:48px;background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;position:relative;z-index:2}.hero-orb span{font-size:72px;color:#a5b4fc;filter:drop-shadow(0 14px 22px rgba(0,0,0,.18))}.stats-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:15px}.metric-card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:18px;box-shadow:var(--shadow)}.metric-card.danger strong{color:#dc2626}.metric-top{display:flex;align-items:center;gap:10px;color:#64748b;font-size:12px;font-weight:700}.metric-icon{width:34px;height:34px;border-radius:10px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;font-weight:800}.metric-card strong{font-size:28px;color:var(--navy);display:block;margin:16px 0 6px}.metric-card small{color:#94a3b8}.dashboard-grid{display:grid;gap:22px}.two-col{grid-template-columns:repeat(2,minmax(0,1fr))}.panel{background:#fff;border:1px solid var(--border);border-radius:18px;padding:22px;box-shadow:var(--shadow)}.panel h3{margin:0;color:var(--navy);font-size:17px}.panel-head{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:18px}.panel-head h3{margin:0}.panel-head p{margin:5px 0 0;color:#94a3b8;font-size:12px}.text-btn,.link-btn{border:0;background:transparent;color:var(--indigo);font-weight:700;padding:6px}.contract-list,.analysis-list{display:flex;flex-direction:column}.list-row{display:flex;align-items:center;gap:11px;padding:13px 0;border-top:1px solid #eef1f5}.list-row:first-child{border-top:0}.row-icon{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;flex:none}.row-icon.doc{background:#eef7ff;color:#2563eb}.row-icon.analysis{background:#f0edff;color:#7c3aed}.row-main{min-width:0;flex:1}.row-main strong{display:block;font-size:13px;color:#1e293b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.row-main small{display:block;color:#94a3b8;font-size:10px;margin-top:3px}.score-badge{display:flex;align-items:center;gap:6px}.score-badge strong{font-size:14px;color:var(--navy)}.mini-btn{border:1px solid var(--border);background:#fff;color:#334155;padding:7px 10px;border-radius:8px;font-size:11px;font-weight:800}.mini-btn:hover{border-color:#c9cfff;color:var(--indigo)}.primary-mini{border-color:#d2d6ff;background:#eef0ff;color:var(--indigo)}.workflow-panel{padding:24px}.workflow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.workflow-step{display:flex;gap:12px;padding:16px;background:#fafbfe;border:1px solid var(--border);border-radius:13px}.workflow-step>span{font-weight:800;color:var(--indigo);font-size:12px}.workflow-step strong{display:block;font-size:13px}.workflow-step small{display:block;color:#94a3b8;margin-top:4px;font-size:11px}.section-intro{display:flex;align-items:center;justify-content:space-between;gap:15px}.section-intro h1{font-size:28px;color:var(--navy);margin:0}.section-intro p{color:#64748b;margin:7px 0 0}.primary-btn,.secondary-btn,.ghost-btn{border:0;border-radius:10px;padding:11px 15px;font-weight:800;font-size:12px}.primary-btn{background:linear-gradient(90deg,#5b5cf0,#6d57f8);color:#fff;box-shadow:0 10px 20px rgba(91,92,240,.18)}.secondary-btn{background:#fff;color:var(--indigo);border:1px solid #cfd4ff}.ghost-btn{background:#fff;color:var(--indigo)}.ghost-btn.light{background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.18)}.full{width:100%}.stack-form{display:flex;flex-direction:column;gap:13px}.stack-form label,.panel label{display:flex;flex-direction:column;gap:7px;color:#475569;font-weight:700;font-size:12px}.stack-form input,.stack-form textarea,.stack-form select,.panel input,.panel textarea,.panel select,.assistant-panel select,.assistant-panel textarea{border:1px solid #dce1ea;background:#fbfcfe;border-radius:10px;padding:11px 12px;outline:none;resize:vertical}.stack-form input:focus,.stack-form textarea:focus,.stack-form select:focus,.panel input:focus,.panel textarea:focus,.panel select:focus{border-color:#aeb6ff;box-shadow:0 0 0 3px #eef0ff}.file-input{padding:9px!important}.file-chip{padding:9px 11px;background:#f4f6ff;color:#4f46e5;border:1px solid #e6e7ff;border-radius:9px;font-size:11px}.alert{margin-top:14px;padding:11px 12px;border-radius:9px;font-size:12px}.alert.success{background:#ecfdf5;color:#166534;border:1px solid #bbf7d0}.alert.danger{background:#fff1f2;color:#9f1239;border:1px solid #fecdd3}.table-wrap{width:100%;overflow:auto}.data-table{width:100%;border-collapse:collapse;min-width:760px}.data-table th{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;text-align:left;padding:11px;border-bottom:1px solid var(--border)}.data-table td{padding:14px 11px;border-bottom:1px solid #f0f2f6;color:#475569;font-size:12px;vertical-align:middle}.data-table tr:last-child td{border-bottom:0}.data-table small{display:block;color:#94a3b8;font-size:10px;margin-top:4px}.table-title{display:flex;align-items:center;gap:9px}.table-actions{display:flex;gap:7px;flex-wrap:wrap}.table-score{font-size:15px;color:var(--navy)}.muted-small{color:#94a3b8;font-size:10px}.pill{display:inline-flex;align-items:center;padding:6px 9px;border-radius:999px;font-size:10px;font-weight:800}.pill.neutral{background:#f1f5f9;color:#64748b}.purple-pill{background:#efedff;color:#6742d8}.risk-pill{display:inline-flex;align-items:center;justify-content:center;padding:5px 8px;border-radius:999px;font-size:9px;font-weight:900}.risk-pill.large{padding:7px 12px;font-size:10px}.low-risk{color:#166534;background:var(--green-bg)}.medium-risk{color:#a16207;background:var(--amber-bg)}.high-risk{color:#b91c1c;background:var(--red-bg)}.neutral-risk{color:#475569;background:#f1f5f9}.upload-panel{min-height:100%}.section-icon{width:44px;height:44px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;margin-bottom:14px}.section-icon.blue{background:#ecf5ff;color:#2563eb}.section-icon.purple{background:#f0edff;color:#6d45d8}.details-panel{overflow:hidden}.contract-meta-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}.contract-meta-grid>div{background:#f8fafc;border:1px solid var(--border);border-radius:10px;padding:12px}.contract-meta-grid span{display:block;color:#94a3b8;font-size:10px}.contract-meta-grid strong{display:block;font-size:12px;margin-top:5px}.document-viewer{background:#0f172a;color:#dbeafe;border-radius:14px;padding:20px;max-height:530px;overflow:auto;white-space:pre-wrap;line-height:1.65;font-size:12px}.document-viewer.small{max-height:360px}.analysis-hero-panel{display:grid;grid-template-columns:1fr 250px;gap:15px;background:linear-gradient(115deg,#111a3f,#27386d 68%,#4f46e5);border-radius:20px;padding:28px;color:#fff}.analysis-hero-main h2{font-size:28px;margin:12px 0 8px}.analysis-hero-main p{margin:0;color:#dbe7ff}.risk-score-card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.13);border-radius:15px;padding:18px}.risk-score-card span{display:block;color:#c7d2fe;font-size:11px}.risk-score-card strong{display:block;font-size:38px;margin:7px 0 8px}.risk-score-card .risk-pill{width:max-content}.empty-analysis{background:#fff;border:1px dashed #d9deea;border-radius:18px;padding:55px 22px;text-align:center}.empty-icon{width:62px;height:62px;border-radius:18px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;margin:0 auto 14px;font-size:24px}.empty-analysis h3{margin:0;color:var(--navy)}.empty-analysis p,.muted{color:#94a3b8}.long-text{color:#475569;line-height:1.8;margin:0}.category-card{border:1px solid var(--border);border-radius:13px;padding:15px;background:#fbfcff}.category-card+.category-card{margin-top:10px}.category-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.category-meter{height:6px;background:#eef1f7;border-radius:999px;margin:11px 0;overflow:hidden}.category-meter span{display:block;height:100%;background:linear-gradient(90deg,#5b5cf0,#22c5d5);border-radius:999px}.category-card p,.insight-card p,.recommendation-card p,.clause-section p{color:#64748b;line-height:1.6;font-size:12px;margin:8px 0}.category-card small{color:#94a3b8}.chip-list{display:flex;flex-direction:column;gap:10px;margin-top:15px}.category-risk-panel{padding-bottom:26px}.category-risk-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:15px}.scoreboard-panel{background:linear-gradient(135deg,#101a3b 0%,#25376d 58%,#4f46e5 100%);border-radius:20px;padding:24px;color:#fff;box-shadow:0 18px 45px rgba(17,24,39,.16)}.scoreboard-header{display:flex;justify-content:space-between;align-items:center;gap:22px}.scoreboard-eyebrow{color:#dbe7ff;opacity:.75}.scoreboard-header h3{margin:7px 0 4px;color:#fff;font-size:20px}.scoreboard-header p{margin:0;color:#cbd5e1;font-size:12px}.scoreboard-total{min-width:170px;padding:15px 18px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);border-radius:14px;text-align:center}.scoreboard-total span{display:block;color:#cbd5e1;font-size:10px;text-transform:uppercase;letter-spacing:.08em;font-weight:800}.scoreboard-total strong{display:block;font-size:30px;margin:6px 0 6px;color:#fff}.scoreboard-total .risk-pill{background:#fff}.scoreboard-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}.scoreboard-item{padding:16px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.07);border-radius:13px}.scoreboard-item span{display:block;color:#cbd5e1;font-size:10px;text-transform:uppercase;letter-spacing:.07em;font-weight:800}.scoreboard-item strong{display:block;color:#fff;font-size:27px;margin:9px 0 2px}.scoreboard-item small{color:#cbd5e1;font-size:10px}.insight-card{padding:14px;border:1px solid var(--border);border-radius:12px;background:#fbfcff}.insight-card strong{font-size:13px;color:var(--navy)}.clause-list{display:flex;flex-direction:column;gap:12px;margin-top:15px}.clause-card{border:1px solid var(--border);border-radius:13px;padding:17px;background:#fff}.clause-section span,.revision-box span{display:block;font-size:10px;font-weight:900;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;margin-bottom:7px}.clause-section blockquote{margin:0;padding:11px 13px;background:#f7f8fc;border-left:3px solid #a5b4fc;border-radius:8px;color:#475569;line-height:1.6;font-size:12px}.revision-box{margin-top:12px;background:#eef6ff;border:1px solid #dbeafe;border-radius:10px;padding:12px}.revision-box p{margin:0;color:#334155;line-height:1.6;font-size:12px}.recommendation-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:15px}.recommendation-card{display:grid;grid-template-columns:38px 1fr;gap:12px;padding:15px;border:1px solid var(--border);border-radius:12px;background:#fbfcff}.recommendation-number{font-weight:900;color:#7c5cff}.recommendation-card strong{color:var(--navy)}.qa-layout{display:grid;grid-template-columns:410px 1fr;gap:22px}.qa-compose{height:fit-content}.prompt-chips{display:flex;gap:7px;flex-wrap:wrap;margin:-2px 0 4px}.prompt-chips button{border:1px solid #e1e5ef;background:#fff;color:#64748b;border-radius:999px;padding:7px 9px;font-size:10px}.answer-panel{min-height:520px}.answer-box{background:linear-gradient(180deg,#f8f9ff,#fff);border:1px solid #e6e8f3;border-radius:14px;padding:18px;line-height:1.8;color:#334155;min-height:160px}.subheading{margin:22px 0 10px;color:var(--navy)}.sources-details{margin-top:18px;border:1px solid var(--border);border-radius:12px;background:#fbfcff;overflow:hidden}.sources-details summary{cursor:pointer;list-style:none;padding:12px 14px;color:var(--navy);font-size:12px;font-weight:800}.sources-details summary::-webkit-details-marker{display:none}.sources-details summary:after{content:"▾";float:right;color:#94a3b8}.sources-details[open] summary:after{content:"▴"}.sources-details .document-viewer{margin:0 12px 12px}.assistant-panel{position:fixed;right:25px;bottom:92px;width:350px;background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:0 25px 60px rgba(15,23,42,.18);z-index:80;overflow:hidden}.assistant-head{padding:15px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);background:linear-gradient(90deg,#f9f8ff,#f4fbff)}.assistant-head strong{display:block;color:var(--navy);font-size:13px}.assistant-head small{display:block;color:#94a3b8;font-size:10px;margin-top:2px}.assistant-head button{border:0;background:transparent;font-size:22px;color:#94a3b8}.assistant-body{padding:16px}.assistant-body select,.assistant-body textarea{width:100%;margin-top:8px;margin-bottom:10px}.ai-fab{position:fixed;right:26px;bottom:25px;width:54px;height:54px;border:0;border-radius:17px;background:linear-gradient(135deg,#5b5cf0,#18c1d8);color:#fff;font-size:24px;box-shadow:0 16px 30px rgba(91,92,240,.32);z-index:75}.confirm-overlay{position:fixed;inset:0;background:rgba(15,23,42,.42);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;z-index:120;padding:24px}.confirm-modal,.about-modal{width:min(460px,100%);background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:0 28px 70px rgba(15,23,42,.24);padding:24px}.confirm-modal{text-align:center}.confirm-icon{width:46px;height:46px;border-radius:14px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-size:20px}.confirm-modal h3{margin:0;color:var(--navy);font-size:20px}.confirm-modal p{color:#64748b;line-height:1.6;font-size:12px}.confirm-actions{display:flex;justify-content:center;gap:10px;margin-top:20px}.confirm-actions .secondary-btn,.confirm-actions .primary-btn{min-width:100px}.confirm-head{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid var(--border);padding-bottom:14px}.confirm-head strong{display:block;color:var(--navy);font-size:15px}.confirm-head small{display:block;color:#94a3b8;font-size:10px;margin-top:3px}.about-modal-body{padding-top:16px;color:#475569;font-size:12px;line-height:1.7}.about-list{display:flex;flex-direction:column;margin-top:12px;border:1px solid var(--border);border-radius:12px;overflow:hidden}.about-row{border:0;border-bottom:1px solid #edf0f4;background:#fff;padding:14px;display:flex;justify-content:space-between;align-items:center;color:#334155;font-weight:700;font-size:12px;text-align:left}.about-row:last-child{border-bottom:0}.about-row:hover{background:#f8f9ff;color:var(--indigo)}.about-row strong{color:#94a3b8;font-size:18px}.sidebar-bottom{margin-top:auto} .settings-card{min-height:220px}.setting-icon{width:42px;height:42px;border-radius:12px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;margin-bottom:12px}.setting-row,.health-item{display:flex;justify-content:space-between;gap:10px;padding:12px 0;border-top:1px solid #edf0f4;font-size:12px}.setting-row span,.health-item span{color:#94a3b8}.setting-row strong{color:var(--navy);text-align:right}.health-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:15px}.health-item{border:1px solid var(--border);border-radius:11px;padding:14px;display:block;background:#fbfcff}.health-item strong{display:block;color:#166534;margin-top:8px}.settings-tech-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:15px}.tech-card{border:1px solid var(--border);border-radius:12px;background:#fbfcff;padding:15px}.tech-card span{display:block;color:#94a3b8;font-size:10px;text-transform:uppercase;letter-spacing:.06em;font-weight:800}.tech-card strong{display:block;color:var(--navy);font-size:12px;margin-top:8px;line-height:1.4}.contract-help-panel{margin-top:0}.contract-answer-box{margin-top:16px}.help-grid-three{grid-template-columns:repeat(3,minmax(0,1fr))}.disclaimer,.mini-disclaimer{background:#fff7ed;color:#7c2d12;border:1px solid #fed7aa;border-radius:10px;padding:12px;font-size:11px;line-height:1.6}.empty-state{padding:36px 10px;text-align:center;color:#94a3b8;font-size:12px}.empty-dot{width:30px;height:30px;border-radius:10px;background:#f1f5f9;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;color:#64748b}.auth-page{min-height:100vh;background:linear-gradient(135deg,#eef1ff 0%,#f8fbff 45%,#f2fcff 100%);display:flex;align-items:center;justify-content:center;padding:30px;position:relative;overflow:hidden}.auth-shell{width:min(1080px,100%);display:grid;grid-template-columns:1.05fr .95fr;background:#fff;border:1px solid rgba(255,255,255,.7);border-radius:28px;overflow:hidden;box-shadow:0 28px 80px rgba(23,37,84,.12);position:relative;z-index:2}.auth-hero{padding:54px;color:#fff;background:linear-gradient(140deg,#111b43,#27396e 65%,#4f46e5);position:relative}.auth-hero:after{content:"";position:absolute;width:420px;height:420px;border-radius:50%;right:-180px;top:-170px;background:radial-gradient(circle,rgba(45,220,255,.25),transparent 65%)}.auth-hero h1{font-size:46px;line-height:1.06;margin:0 0 16px;max-width:500px;position:relative;z-index:2}.auth-hero p{max-width:560px;line-height:1.8;color:#dbe7ff;position:relative;z-index:2}.hero-points{display:flex;flex-wrap:wrap;gap:8px;margin-top:25px;position:relative;z-index:2}.hero-points span{padding:8px 10px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);border-radius:999px;font-size:10px}.auth-card{padding:45px}.auth-card h2{margin:35px 0 8px;color:var(--navy);font-size:28px}.auth-card .brand-row small{font-size:10px}.auth-switch{margin-top:20px;text-align:center;color:#64748b;font-size:12px}.mini-disclaimer{margin-top:22px}.auth-glow{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}.glow-one{width:260px;height:260px;background:#c4b5fd;left:-100px;top:10%}.glow-two{width:300px;height:300px;background:#bae6fd;right:-120px;bottom:0}.sidebar-backdrop{display:none}
.upload-options{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.upload-option{border:1px solid var(--border);background:#fbfcff;border-radius:12px;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;color:#475569;transition:.15s}.upload-option:hover{border-color:#cbd1ff;background:#f5f5ff;color:var(--indigo);transform:translateY(-1px)}.upload-option span{width:34px;height:34px;border-radius:10px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;font-weight:900}.upload-option strong{font-size:11px}.upload-option small{font-size:9px;color:#94a3b8}.hidden-file-input{display:none}.scan-chip{background:#eefcf7;color:#047857;border-color:#d1fae5}.camera-overlay{position:fixed;inset:0;background:rgba(15,23,42,.65);display:flex;align-items:center;justify-content:center;padding:20px;z-index:100}.camera-modal{width:min(720px,100%);background:#fff;border-radius:20px;box-shadow:0 30px 80px rgba(15,23,42,.3);overflow:hidden}.camera-head{padding:16px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border)}.camera-head strong{display:block;color:var(--navy);font-size:14px}.camera-head small{display:block;color:#94a3b8;font-size:10px;margin-top:4px}.camera-close{border:0;background:transparent;color:#64748b;font-size:24px}.camera-frame{background:#0b1225;padding:18px}.camera-frame video{display:block;width:100%;max-height:65vh;object-fit:contain;border-radius:12px;background:#000}.camera-actions{display:flex;justify-content:flex-end;gap:9px;padding:16px 18px}.camera-actions .secondary-btn,.camera-actions .primary-btn{min-width:130px}
@media (max-width:1100px){.stats-grid{grid-template-columns:repeat(2,1fr)}.two-col,.qa-layout{grid-template-columns:1fr}.recommendation-grid{grid-template-columns:1fr}.health-grid{grid-template-columns:repeat(2,1fr)}.category-risk-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.scoreboard-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.scoreboard-header{align-items:flex-start;flex-direction:column}.scoreboard-total{width:100%}}
.help-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}.help-item{display:flex;gap:10px;padding:13px;border:1px solid var(--border);background:#fbfcff;border-radius:12px}.help-item>span{width:28px;height:28px;flex:0 0 28px;border-radius:9px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:11px}.help-item strong{display:block;color:var(--navy);font-size:12px}.help-item p{margin:4px 0 0;color:#94a3b8;font-size:11px;line-height:1.5}.upload-progress{margin-top:4px;padding:11px 12px;border:1px solid #e1e5f3;background:#fafbff;border-radius:11px}.upload-progress-line{display:flex;align-items:center;gap:8px;color:#475569;font-size:11px;font-weight:800}.progress-dot{width:8px;height:8px;border-radius:50%;background:#cbd5e1}.progress-dot.active{background:#5b5cf0;box-shadow:0 0 0 4px #eef0ff}.progress-track{height:5px;border-radius:999px;background:#edf0f7;overflow:hidden;margin-top:9px}.progress-fill{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#5b5cf0,#24b7d7);transition:width .2s ease}.check-list{display:flex;flex-direction:column;gap:10px;margin-top:15px}.check-list div{padding:11px 12px;border-radius:10px;background:#f8fafc;border:1px solid #edf0f4;color:#475569;font-size:12px}.question-tools,.assistant-voice-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:8px 0 10px}.voice-btn{border:1px solid #d9dff0;background:#fff;color:#4f46e5;border-radius:10px;padding:8px 11px;font-size:11px;font-weight:800}.voice-btn:hover{border-color:#b8bdf7;background:#f7f7ff}.voice-btn.listening{background:#fff0f0;color:#b91c1c;border-color:#fecaca}.voice-btn.small{padding:6px 9px;font-size:10px}.answer-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:9px}.answer-toolbar strong{color:var(--navy);font-size:12px}.muted-small{color:#94a3b8;font-size:10px}.assistant-body .voice-btn{margin-bottom:8px}
.sidebar::-webkit-scrollbar{width:7px}.sidebar::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:999px}.sidebar::-webkit-scrollbar-track{background:transparent}@media (max-width:820px){.sidebar{transform:translateX(-100%);transition:.2s}.sidebar.open{transform:translateX(0)}.sidebar-backdrop{display:block;position:fixed;inset:0;background:rgba(15,23,42,.25);border:0;z-index:25}.main-area{margin-left:0}.mobile-menu{display:block;margin-right:10px}.topbar{padding:0 18px}.user-copy{display:none}.content-wrap{padding:18px}.hero-banner{padding:28px}.hero-orb{display:none}.hero-banner h1{font-size:28px}.auth-shell{grid-template-columns:1fr}.auth-hero{display:none}.auth-card{padding:30px}.contract-meta-grid{grid-template-columns:1fr}.analysis-hero-panel{grid-template-columns:1fr}.assistant-panel{right:15px;left:15px;width:auto}.ai-fab{right:15px}.stats-grid{grid-template-columns:1fr 1fr}.help-grid{grid-template-columns:1fr}.help-grid-three{grid-template-columns:1fr}.settings-tech-grid{grid-template-columns:1fr 1fr}.scoreboard-grid{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.stats-grid{grid-template-columns:1fr}.health-grid{grid-template-columns:1fr}.category-risk-grid{grid-template-columns:1fr}.scoreboard-grid{grid-template-columns:1fr}.section-intro{align-items:flex-start;flex-direction:column}.topbar-actions .icon-btn{display:none}.hero-actions{width:100%}.hero-actions .primary-btn,.hero-actions .ghost-btn{flex:1}.workflow{grid-template-columns:1fr 1fr}.data-table{min-width:650px}}
.forgot-link{align-self:flex-end;border:0;background:transparent;color:#5b5cf0;font-size:11px;font-weight:800;padding:0;cursor:pointer}.forgot-link:hover{text-decoration:underline}.recovery-note{padding:11px 12px;border:1px solid #e0e7ff;background:#f7f8ff;border-radius:10px;color:#64748b;font-size:10px;line-height:1.6}.recovery-note strong{color:#4f46e5}.recovery-box{margin-top:16px;border:1px solid #e1e5ef;background:#fbfcff;border-radius:13px;padding:14px}.recovery-box>div:first-child strong{display:block;color:var(--navy);font-size:12px}.recovery-box>div:first-child p{margin:6px 0 12px;color:#94a3b8;font-size:10px;line-height:1.6}.recovery-box>div:first-child p strong{display:inline;color:#5b5cf0}.recovery-code-row{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:10px 0;padding:12px;background:#111a3f;border-radius:10px}.recovery-code-row code{color:#fff;font-size:13px;letter-spacing:.12em;font-weight:900}.recovery-empty{padding:11px 12px;margin:10px 0;background:#f1f5f9;border-radius:9px;color:#94a3b8;font-size:10px}.recovery-box .alert{margin-bottom:0}
.language-source-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}.language-source-head strong{font-size:12px;color:#334155}.upload-document-btn{display:inline-flex;align-items:center;justify-content:center;padding:9px 12px;border:1px solid #c7d2fe;background:#eef0ff;color:#4f46e5;border-radius:10px;font-size:11px;font-weight:800;cursor:pointer}.upload-document-btn:hover{background:#e5e7ff}.upload-document-btn input{display:none}.language-file-chip{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 8px;padding:8px 10px;background:#f8fafc;border:1px solid var(--border);border-radius:10px;font-size:11px;color:#475569}.language-file-chip button{border:0;background:transparent;color:#4f46e5;font-weight:800;font-size:10px;cursor:pointer}.language-file-help{font-size:10px;line-height:1.5;color:#94a3b8;margin:6px 0 0}.password-wrap{position:relative;display:flex;align-items:center}.password-wrap input{width:100%;padding-right:48px!important}.password-toggle{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:32px;height:32px;border:0;background:transparent;color:#64748b;font-size:17px;border-radius:8px}.password-toggle:hover{background:#eef0ff;color:#4f46e5}.password-hint{font-size:10px;line-height:1.5;color:#94a3b8;margin-top:-4px}

.document-generator-grid{align-items:stretch}.document-generator-grid select{width:100%;padding:12px 14px;border:1px solid var(--border);border-radius:12px;background:#fff;color:var(--text);outline:none}.document-generator-grid select:focus,.document-generator-grid textarea:focus{border-color:var(--indigo);box-shadow:0 0 0 3px rgba(91,92,240,.08)}.document-output-panel{min-height:620px}.generated-document{margin:0;min-height:520px;max-height:680px;overflow:auto;white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;font-size:13px;line-height:1.65;color:#1f2937;background:#f8f9fd;border:1px solid var(--border);border-radius:14px;padding:20px}.generator-empty{min-height:520px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--muted);padding:30px}.generator-empty h3{color:var(--text);margin:12px 0 6px}.generator-note{margin-top:16px;padding:14px 16px;border:1px solid var(--border);background:var(--soft);border-radius:12px;display:flex;flex-direction:column;gap:4px}.generator-note span{color:var(--muted);font-size:13px}
.evidence-list{display:grid;gap:14px;margin-top:14px}.evidence-card{border:1px solid var(--border);background:#f8fafc;border-radius:18px;padding:18px}.evidence-meta{display:block;margin-top:5px;color:#64748b;font-size:12px}.evidence-source-box{margin-top:14px;background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px}.evidence-source-box span,.evidence-context-box span{display:block;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:#6366f1;margin-bottom:7px}.evidence-source-box blockquote,.evidence-context-box blockquote{margin:0;color:#334155;line-height:1.65;white-space:pre-wrap}.evidence-meta-row{display:flex;gap:10px;justify-content:space-between;flex-wrap:wrap;margin-top:10px;font-size:12px;color:#64748b}.evidence-meta-row.warning{color:#b45309}.compact-actions{margin-top:0}
.activity-list{display:flex;flex-direction:column;gap:0;border:1px solid var(--border);border-radius:14px;overflow:hidden;background:#fff}.activity-row{display:grid;grid-template-columns:36px minmax(0,1fr) auto;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid var(--border);background:#fff}.activity-row:last-child{border-bottom:0}.activity-row:hover{background:#fafbff}.activity-icon{width:34px;height:34px;border-radius:10px;background:#eef0ff;color:var(--indigo);display:flex;align-items:center;justify-content:center;font-weight:900}.activity-main{min-width:0}.activity-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.activity-top strong{color:var(--navy);font-size:12px}.activity-main p{margin:4px 0 2px;color:#475569;font-size:11px}.activity-main small{display:block;color:#94a3b8;font-size:9px;word-break:break-all}.activity-row time{white-space:nowrap;color:#64748b;font-size:10px}.activity-status{display:inline-flex;align-items:center;justify-content:center;min-width:34px;padding:4px 7px;border-radius:999px;font-size:9px;font-weight:800}.activity-status.ok{background:#ecfdf5;color:#047857}.activity-status.problem{background:#fff1f2;color:#be123c}@media (max-width:700px){.activity-row{grid-template-columns:32px minmax(0,1fr)}.activity-row time{grid-column:2}.activity-row{padding:12px}}

`;

export default App;

