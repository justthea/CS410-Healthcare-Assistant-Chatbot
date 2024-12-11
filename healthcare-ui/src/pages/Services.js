import React from 'react';
import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';

const Services = () => {
  const services = [
    { name: 'General Checkups', description: 'Routine health assessments for individuals of all ages.' },
    { name: 'Pediatrics', description: 'Specialized care for children and adolescents.' },
    { name: 'Cardiology', description: 'Heart health consultations and diagnostics.' },
    { name: 'Diagnostics', description: 'Laboratory tests and medical imaging services.' },
    { name: 'Physical Therapy', description: 'Rehabilitation services to restore mobility and strength.' },
  ];

  return (
    <Box sx={{ padding: '2rem'}}>
      <Typography variant="h4" gutterBottom>
        Our Services
      </Typography>
      <List>
        {services.map((service, index) => (
          <ListItem key={index} sx={{ marginBottom: '1rem' }}>
            <ListItemText
              primary={service.name}
              secondary={service.description}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Services;

