// Navbar.js
import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';

function AppNavbar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="#home">Welcome to Confessions</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;
