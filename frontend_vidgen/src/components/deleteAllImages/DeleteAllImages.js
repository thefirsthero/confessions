import React, { useState } from 'react';
import axios from 'axios';

function DeleteAllImages() {
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const handleDelete = () => {
    if (confirmDelete) {
      // Make a DELETE request to delete all images
      // Get the base API URL from .env
      const baseUrl = process.env.REACT_APP_API_URL;

      // Append the specific endpoint
      const apiUrl = `${baseUrl}/delete-images/`;
      axios.delete(apiUrl)
        .then(() => {
          setSuccess('All images deleted successfully');
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
      <h2>Delete All Images</h2>
      <button onClick={() => setConfirmDelete(true)}>Delete All Images</button>
      {success && <p>{success}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default DeleteAllImages;
