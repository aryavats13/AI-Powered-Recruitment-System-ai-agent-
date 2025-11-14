import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadResume = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    window.location.href = `/candidate/${data.candidate_id}`;

  };

  return (
    <div style={{ padding: "30px", fontFamily: "sans-serif" }}>
      <h1>Resume Analyzer</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadResume} style={{ marginLeft: "10px" }}>
        Upload
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Extracted Info</h2>
          <p><b>Email:</b> {result.email}</p>
          <p><b>Phone:</b> {result.phone}</p>

          <p><b>Skills:</b></p>
          <ul>
            {result.skills.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>

          <p><b>Experience:</b></p>
          <pre>{result.experience}</pre>

          <p><b>Projects:</b></p>
          <pre>{result.projects}</pre>

          <p><b>Education:</b></p>
          <pre>{result.education}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
