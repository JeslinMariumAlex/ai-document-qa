import { useState } from "react";
import './App.css'

function App() {

  const [selectedFile, setSelectedFile] = useState(null);

  return (
     <div>
      <h1>AI Document Q&A</h1>

      <h2>Upload a PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(event) => setSelectedFile(event.target.files[0])}
      />

      {selectedFile && (
        <p>Selected file: {selectedFile.name}</p>
      )}
    </div>
  )
}

export default App
