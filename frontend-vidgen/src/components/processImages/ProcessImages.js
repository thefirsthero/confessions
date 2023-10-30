import React, { useState } from 'react';
import axios from 'axios';

function ProcessImages() {
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const handleProcess = () => {
    // Make a GET request to process images and download the result
    // Get the base API URL from .env
    const baseUrl = process.env.REACT_APP_API_URL;

    // Append the specific endpoint
    const apiUrl = `${baseUrl}/process-images`;
    axios.get(apiUrl)
      .then((response) => {
        // Process the response or initiate a download as needed
        // Example: window.open(response.data.downloadUrl, '_blank');
        setSuccess('Images processed successfully');
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
        setSuccess(null);
      });
  };

  return (
    <div>
      <h2>Process Images</h2>
      <button onClick={handleProcess}>Process Images</button>
      {success && <p>{success}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default ProcessImages;
