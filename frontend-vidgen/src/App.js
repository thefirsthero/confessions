import React, { useState } from 'react';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import ListImages from './components/listImages/ListImages'; // You'll need to create separate components for each action
import UploadImages from './components/uploadImages/UploadImages';
import DeleteAllImages from './components/deleteAllImages/DeleteAllImages';
import DeleteSpecificImage from './components/deleteSpecificImage/DeleteSpecificImage';
import ProcessImages from './components/processImages/ProcessImages';

function App() {
  const [key, setKey] = useState('list-images'); // The initial active tab

  return (
    <Tabs id="controlled-tab-example" activeKey={key} onSelect={(k) => setKey(k)}>
      <Tab eventKey="list-images" title="List Images">
        <ListImages />
      </Tab>
      <Tab eventKey="upload-images" title="Upload Images">
        <UploadImages />
      </Tab>
      <Tab eventKey="delete-all-images" title="Delete all Images">
        <DeleteAllImages />
      </Tab>
      <Tab eventKey="delete-specific-image" title="Delete Specific Image">
        <DeleteSpecificImage />
      </Tab>
      <Tab eventKey="process-images" title="Process Images">
        <ProcessImages />
      </Tab>
    </Tabs>
  );
}

export default App;
