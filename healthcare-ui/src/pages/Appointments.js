import React from 'react';
import { Box, Typography, TextField, Button } from '@mui/material';

const Appointments = () => {
  return (
    <Box sx={{ padding: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Schedule an Appointment
      </Typography>
      <Typography variant="body1" gutterBottom>
        Please fill out the form below to book your appointment. Our team will contact you shortly to confirm your visit.
      </Typography>
      <Box sx={{ marginTop: '2rem' }}>
        <TextField fullWidth label="Full Name" variant="outlined" sx={{ marginBottom: '1rem' }} />
        <TextField fullWidth label="Email" variant="outlined" sx={{ marginBottom: '1rem' }} />
        <TextField fullWidth label="Phone Number" variant="outlined" sx={{ marginBottom: '1rem' }} />
        <TextField
          fullWidth
          label="Preferred Date and Time"
          variant="outlined"
          sx={{ marginBottom: '1rem' }}
        />
        <Button variant="contained" color="primary">
          Book Appointment
        </Button>
      </Box>
    </Box>
  );
};

export default Appointments;
