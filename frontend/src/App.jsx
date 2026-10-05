import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [documentId, setDocumentId] = useState(null);
  const [answer, setAnswer] = useState("");
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const handleUpload = async () => {
    setUploading(true);

    try {
      console.log(selectedFile);

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch("http://127.0.0.1:8000/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Upload failed");
        setUploading(false);
        return;
      }

      setDocumentId(data.document_id);
      setMessage(`Upload successful! Document ID: ${data.document_id}`);
      setSelectedFile(null);
      fileInputRef.current.value = "";
      fetchDocuments(); // Refresh the list of documents
      setUploading(false);
    } catch (error) {
      setMessage("Could not connect to the server");
      setUploading(false);
    }
  };

  const fetchDocuments = async () => {
    const response = await fetch("http://127.0.0.1:8000/documents");

    const data = await response.json();

    setDocuments(data);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleAsk = async () => {
    setAsking(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          document_id: documentId,
          question: question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setAnswer(data.detail || "Something went wrong");
        setAsking(false);
        return;
      }

      setAnswer(data.answer);
      setQuestion("");
      setAsking(false);
    } catch (error) {
      setAnswer("Could not connect to the server");
      setAsking(false);
    }
  };

  return (
    <div className="app-container">
      <h1>AI Document Q&A</h1>
      <h2>Upload a PDF</h2>

      <div className="upload-section">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={(event) => setSelectedFile(event.target.files[0])}
        />

        {selectedFile && <p>Selected file: {selectedFile.name}</p>}

        <button onClick={handleUpload} disabled={!selectedFile || uploading}>
          {uploading ? "Uploading..." : "Upload PDF"}
        </button>
      </div>

      {message && <p>{message}</p>}

      <div className="main-content">
        <div className="documents-section">
          <h2>Documents</h2>

          <div className="document-list">
            {documents.map((document) => (
              <div key={document.document_id}>
                <button
                  className={
                    documentId === document.document_id
                      ? "selected-document"
                      : ""
                  }
                  onClick={() => setDocumentId(document.document_id)}
                >
                  {document.filename}
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="qa-section">
          <h2>Ask a question</h2>

          <div className="question-section">
            <input
              type="text"
              placeholder="Ask something about the document..."
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  documentId &&
                  question.trim() &&
                  !asking
                ) {
                  handleAsk();
                }
              }}
            />

            <button
              onClick={handleAsk}
              disabled={!documentId || !question.trim() || asking}
            >
              {asking ? "Asking..." : "Ask"}
            </button>
          </div>

          {answer && (
            <div className="answer-section">
              <h3>Answer</h3>
              <p>{answer}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
