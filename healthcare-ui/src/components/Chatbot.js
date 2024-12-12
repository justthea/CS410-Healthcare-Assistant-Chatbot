import React, { useState } from 'react';
import { Box, TextField, IconButton, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/Close';
import { GoogleGenerativeAI } from "@google/generative-ai";

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChatbot = () => setIsOpen(!isOpen);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const genAI = new GoogleGenerativeAI(process.env.REACT_APP_GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: "gemini-pro" });

      const result = await model.generateContent(input);
      const response = await result.response;
      const botMessage = response.text();

      setMessages([...newMessages, { role: 'assistant', content: botMessage }]);
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      setMessages([
        ...newMessages,
        { role: 'assistant', content: 'Sorry, there was an error. Please try again later.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <Box sx={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
        <IconButton
          onClick={toggleChatbot}
          sx={{
            backgroundColor: '#00796b',
            color: 'white',
            width: '50px',
            height: '50px',
            borderRadius: '50%',
            boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
          }}
        >
          💬
        </IconButton>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: '#f9f9f9',
        zIndex: 1200,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box
        sx={{
          padding: '16px',
          backgroundColor: '#00796b',
          color: 'white',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="h6">Chat with us</Typography>
        <IconButton onClick={toggleChatbot} sx={{ color: 'white' }}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
        }}
      >
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '8px',
            }}
          >
            <Box
              sx={{
                padding: '12px',
                borderRadius: '12px',
                backgroundColor: message.role === 'user' ? '#00796b' : '#e0e0e0',
                color: message.role === 'user' ? 'white' : 'black',
                maxWidth: '70%',
              }}
            >
              {message.content}
            </Box>
          </Box>
        ))}
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', padding: '8px' }}>
            <CircularProgress size={24} />
          </Box>
        )}
      </Box>

      <Box
        sx={{
          padding: '16px',
          display: 'flex',
          alignItems: 'center',
          borderTop: '1px solid #ccc',
          backgroundColor: 'white',
        }}
      >
        <TextField
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message"
          fullWidth
          size="small"
          disabled={isLoading}
          sx={{ marginRight: '8px' }}
        />
        <IconButton onClick={handleSend} color="primary" disabled={isLoading}>
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Chatbot;
