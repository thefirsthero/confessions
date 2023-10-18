import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ListImages() {
  const [images, setImages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Make a GET request to fetch a list of images
    // Get the base API URL from .env
    const baseUrl = process.env.REACT_APP_API_URL;

    // Append the specific endpoint
    const apiUrl = `${baseUrl}/list-images`;
    
    axios.get(apiUrl)
      .then((response) => {
        setImages(response.data);
        setError(null);
      })
      .catch((error) => {
        setImages([]);
        setError(error.message);
      });
  }, []);

  return (
    <div>
      <h2>List Images</h2>
      {error && <p>Error: {error}</p>}
      {images.length === 0 && !error && <p>No images available.</p>}
      {images.length > 0 && (
        <ul>
          {images.map((image, index) => (
            <li key={index}>{image.filename}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ListImages;
