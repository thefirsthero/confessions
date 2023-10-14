// Routes.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MakeConfession from './post/Post';
import Feed from './feed/Feed';

function Routes_() {
  return (
    <Routes>
      <Route path="/make-confession" component={MakeConfession} />
      <Route path="/feed" component={Feed} />
      {/* Add more routes if needed */}
    </Routes>
  );
}

export default Routes_;
