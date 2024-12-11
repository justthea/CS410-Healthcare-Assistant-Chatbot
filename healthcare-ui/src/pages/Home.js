import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <Box sx={{ padding: '2rem', textAlign: 'center' }}>

      <Typography variant="h3" gutterBottom>
        Welcome to the Healthcare Company.
      </Typography>
      <Typography variant="h6" gutterBottom>
        Providing compassionate and comprehensive healthcare services to your family.
      </Typography>
      <Typography variant="body1" gutterBottom>
        At Healthcare Company, we are committed to offering personalized care, state-of-the-art facilities, and a team of dedicated professionals to meet all your healthcare needs.
      </Typography>
      <Button
        variant="contained"
        color="primary"
        sx={{ marginTop: '1rem' }}
        component={Link}
        to="/about"
      >Learn More About Us</Button>
    </Box>
  );
};

export default Home;
