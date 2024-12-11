import React from 'react';
import { Box, Typography } from '@mui/material';

const About = () => {
  return (
    <Box sx={{ padding: '2rem', textAlign: 'center'}}>
      <Typography variant="h4" gutterBottom>
        About Us
      </Typography>
      <Typography variant="body1" gutterBottom>
        Established in 2024, the Healthcare Company has been dedicated to delivering high-quality medical services in our community. Our team of experienced professionals strives to ensure the well-being of our patients through cutting-edge technology and personalized care.
      </Typography>
      <Typography variant="h5" gutterBottom>
        Our Mission
      </Typography>
      <Typography variant="body1" gutterBottom>
        To provide accessible, compassionate, and comprehensive healthcare services to improve the quality of life for every individual we serve.
      </Typography>
    </Box>
  );
};

export default About;

