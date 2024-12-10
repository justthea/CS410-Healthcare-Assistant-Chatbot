import React, { useState } from 'react';
import { Box, TextField, IconButton, Typography } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/Close';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false); // To toggle the chatbot
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user's message to chat
    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      
      // Sample post request
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer YOUR_API_KEY`,
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: input }],
        }),
      });

      const data = await response.json();
      const botMessage = data.choices[0].message.content;

      // Add bot's response to chat
      setMessages([...newMessages, { sender: 'bot', text: botMessage }]);
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      setMessages([...newMessages, { sender: 'bot', text: 'Sorry, there was an error.' }]);
    }
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1000,
      }}
    >
      {/* Chatbot Bubble */}
      {isOpen ? (
        <Box
          sx={{
            width: 300,
            height: 400,
            backgroundColor: 'white',
            border: '1px solid #ccc',
            borderRadius: '8px',
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
          }}
        >
          {/* Header */}
          <Box
            sx={{
              padding: '8px',
              backgroundColor: '#00796b',
              color: 'white',
              borderTopLeftRadius: '8px',
              borderTopRightRadius: '8px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Typography variant="subtitle1">Chat with us</Typography>
            <IconButton size="small" onClick={toggleChatbot} sx={{ color: 'white' }}>
              <CloseIcon />
            </IconButton>
          </Box>

          {/* Chat Messages */}
          <Box
            sx={{
              flex: 1,
              overflowY: 'auto',
              padding: '8px',
            }}
          >
            {messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: '8px',
                }}
              >
                <Box
                  sx={{
                    padding: '8px',
                    borderRadius: '8px',
                    backgroundColor: message.sender === 'user' ? '#00796b' : '#f0f0f0',
                    color: message.sender === 'user' ? 'white' : 'black',
                    maxWidth: '80%',
                  }}
                >
                  {message.text}
                </Box>
              </Box>
            ))}
          </Box>

          {/* Input Box */}
          <Box
            sx={{
              padding: '8px',
              display: 'flex',
              alignItems: 'center',
              borderTop: '1px solid #ccc',
            }}
          >
            <TextField
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message"
              fullWidth
              size="small"
              sx={{ marginRight: '8px' }}
            />
            <IconButton onClick={handleSend} color="primary">
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      ) : (
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
      )}
    </Box>
  );
};

export default Chatbot;
