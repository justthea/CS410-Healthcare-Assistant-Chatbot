import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{ padding: '1rem', backgroundColor: '#00796b', color: 'white' }}>
      <Link to="/" style={{ margin: '0 1rem', color: 'white', textDecoration: 'none' }}>Home</Link>
      <Link to="/about" style={{ margin: '0 1rem', color: 'white', textDecoration: 'none' }}>About</Link>
      <Link to="/services" style={{ margin: '0 1rem', color: 'white', textDecoration: 'none' }}>Services</Link>
      <Link to="/contact" style={{ margin: '0 1rem', color: 'white', textDecoration: 'none' }}>Contact</Link>
      <Link to="/appointments" style={{ margin: '0 1rem', color: 'white', textDecoration: 'none' }}>Appointments</Link>
    </nav>
  );
};

export default Navbar;
