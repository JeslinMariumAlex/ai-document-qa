import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    console.log(selectedFile);

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("http://127.0.0.1:8000/documents/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setMessage(`Upload successful! Document ID: ${data.document_id}`);
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
    </div>
  );
}

export default App;
