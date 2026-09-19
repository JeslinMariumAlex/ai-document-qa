import { useState, useEffect } from "react";
import "./App.css";

function App() {
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
      setAsking(false);
    } catch (error) {
      setAnswer("Could not connect to the server");
      setAsking(false);
    }
  };

  return (
    <div>
      <h1>AI Document Q&A</h1>
      <h2>Upload a PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(event) => setSelectedFile(event.target.files[0])}
      />

      {selectedFile && <p>Selected file: {selectedFile.name}</p>}

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload PDF"}
      </button>

      {message && <p>{message}</p>}

      <h2>Documents</h2>

      <div>
        {documents.map((document) => (
          <div key={document.document_id}>
            <button onClick={() => setDocumentId(document.document_id)}>
              {document.filename}
            </button>
          </div>
        ))}
      </div>

      {documentId && <p>Selected document ID: {documentId}</p>}

      <h2>Ask a question</h2>

      <input
        type="text"
        placeholder="Ask something about the document..."
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
      />

      <button
        onClick={handleAsk}
        disabled={!documentId || !question.trim() || asking}
      >
        {asking ? "Asking..." : "Ask"}
      </button>

      {answer && (
        <div>
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
