import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [documentId, setDocumentId] = useState(null);
  const [answer, setAnswer] = useState("");

  const handleUpload = async () => {
    console.log(selectedFile);

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("http://127.0.0.1:8000/documents/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setDocumentId(data.document_id);
    setMessage(`Upload successful! Document ID: ${data.document_id}`);
  };

  const handleAsk = async () => {
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

    setAnswer(data.answer);
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

      <button onClick={handleUpload}>Upload PDF</button>
      {message && <p>{message}</p>}

      <h2>Ask a question</h2>

      <input
        type="text"
        placeholder="Ask something about the document..."
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
      />

      <button onClick={handleAsk}>Ask</button>
      
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
