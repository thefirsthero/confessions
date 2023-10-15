import React, { useState } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import { NavLink } from 'react-router-dom';

function AppNavbar() {
  const [expanded, setExpanded] = useState(false);

  const closeNav = () => {
    setExpanded(false);
  };

  return (
    <Navbar expand="lg" bg="dark" variant="dark" expanded={expanded}>
      <Container>
        <Navbar.Brand href="#home">Welcome to Confessions</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" onClick={() => setExpanded(!expanded)} />
        <Navbar.Collapse id="responsive-navbar-nav" className="justify-content-end">
          <Nav className="ml-auto">
            <Nav.Item>
              <NavLink to="/make-confession" className="nav-link" onClick={closeNav}>
                Make Confession
              </NavLink>
            </Nav.Item>
            <Nav.Item>
              <NavLink to="/feed" className="nav-link" onClick={closeNav}>
                Feed
              </NavLink>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;
