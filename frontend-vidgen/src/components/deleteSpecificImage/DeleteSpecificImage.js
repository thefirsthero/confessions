import React, { useState } from 'react';
import axios from 'axios';

function DeleteSpecificImage() {
  const [filename, setFilename] = useState('');
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const handleDelete = () => {
    if (confirmDelete) {
      // Make a DELETE request to delete a specific image
      // Get the base API URL from .env
      const baseUrl = process.env.REACT_APP_API_URL;

      // Append the specific endpoint
      const apiUrl = `${baseUrl}/delete-image/${filename}`;
      axios.delete(apiUrl)
        .then(() => {
          setSuccess(`Image ${filename} deleted successfully`);
          setError(null);
        })
        .catch((err) => {
          setError(err.message);
          setSuccess(null);
        });
    } else {
      setSuccess(null);
      setError('Please confirm the deletion.');
    }
  };

  return (
    <div>
      <h2>Delete Specific Image</h2>
      <input
        type="text"
        placeholder="Enter filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
      />
      <button onClick={() => setConfirmDelete(true)}>Delete</button>
      {success && <p>{success}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default DeleteSpecificImage;
