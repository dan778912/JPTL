import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [result, setResult] = useState(null);

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);

    try {
      const response = await axios.post('http://localhost:5000/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="App">
      <h1>JLPT Project</h1>
      <form onSubmit={handleFileUpload}>
        <input type="file" id="fileInput" name="file" required />
        <button type="submit">Submit</button>
      </form>
      {result && (
        <div>
          <h2>Results</h2>
          <pre>Original Text: {result.original_text}</pre>
          <div dangerouslySetInnerHTML={{ __html: result.furigana_html }} />
          <pre>Translated Text: {result.translated_text}</pre>
          <pre>Sentiment: {JSON.stringify(result.sentiment, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
