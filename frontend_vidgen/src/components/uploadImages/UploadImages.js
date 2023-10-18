import React, { useState } from 'react';
import axios from 'axios';

function UploadImages() {
  const [file, setFile] = useState(null);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('image', file);

    // Make a POST request to upload the selected image
    // Get the base API URL from .env
    const baseUrl = process.env.REACT_APP_API_URL;

    // Append the specific endpoint
    const apiUrl = `${baseUrl}/upload-images/`;
    axios.post(apiUrl, formData)
      .then(() => {
        setSuccess('Image uploaded successfully');
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
        setSuccess(null);
      });
  };

  return (
    <div>
      <h2>Upload Images</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {success && <p>{success}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default UploadImages;
