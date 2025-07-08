import React, { useState } from "react";
import api from "../api";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please choose a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/files/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (res.status === 201) {
        alert("File uploaded successfully!");
        setFile(null);
      }
    } catch (err) {
      console.error(err);
      setError("Upload failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Upload a file:</label>
        <input type="file" accept=".csv" onChange={handleFileChange} />
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button type="submit">Upload</button>
    </form>
  );
}

export default FileUpload;

