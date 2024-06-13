import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/process', formData, {
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
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} required />
        <button type="submit">Upload</button>
      </form>
      {result && (
        <div>
          <h2>Results</h2>
          <pre>Original Text: {result.original_text}</pre>
          <pre>Hiragana Text: {result.hiragana_text}</pre>
          <pre>Translated Text: {result.translated_text}</pre>
          <pre>Sentiment: {JSON.stringify(result.sentiment, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
