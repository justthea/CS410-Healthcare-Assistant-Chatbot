import React from 'react';
import { Box, Typography, TextField, Button } from '@mui/material';

const Contact = () => {
  return (
    <Box sx={{ padding: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Contact Us
      </Typography>
      <Typography variant="body1" gutterBottom>
        Address: 123 Main Street, City, State, ZIP
      </Typography>
      <Typography variant="body1" gutterBottom>
        Phone: (555) 123-4567
      </Typography>
      <Typography variant="body1" gutterBottom>
        Email: info@healthcare.com
      </Typography>

      <Box sx={{ marginTop: '2rem' }}>
        <Typography variant="h6" gutterBottom>
          Send Us a Message
        </Typography>
        <TextField fullWidth label="Name" variant="outlined" sx={{ marginBottom: '1rem' }} />
        <TextField fullWidth label="Email" variant="outlined" sx={{ marginBottom: '1rem' }} />
        <TextField
          fullWidth
          label="Message"
          variant="outlined"
          multiline
          rows={4}
          sx={{ marginBottom: '1rem' }}
        />
        <Button variant="contained" color="primary">
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default Contact;
