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
      const genAI = new GoogleGenerativeAI('AIzaSyDjuRepuGOLrlHaIVtYXyiDY0Ph5eFvbTM');
      const model = genAI.getGenerativeModel({ model: "gemini-pro" });

      const result = await model.generateContent(input);
      const response = await result.response;
      const botMessage = response.text();

      setMessages([...newMessages, { role: 'assistant', content: botMessage }]);
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      setMessages([...newMessages, { role: 'assistant', content: 'Sorry, there was an error. Please try again later.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
      {isOpen ? (
        <Box sx={{ width: 300, height: 400, backgroundColor: 'white', border: '1px solid #ccc', borderRadius: '8px', display: 'flex', flexDirection: 'column', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
          <Box sx={{ padding: '8px', backgroundColor: '#00796b', color: 'white', borderTopLeftRadius: '8px', borderTopRightRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="subtitle1">Chat with us</Typography>
            <IconButton size="small" onClick={toggleChatbot} sx={{ color: 'white' }}>
              <CloseIcon />
            </IconButton>
          </Box>

          <Box sx={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
            {messages.map((message, index) => (
              <Box key={index} sx={{ display: 'flex', justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: '8px' }}>
                <Box sx={{ padding: '8px', borderRadius: '8px', backgroundColor: message.role === 'user' ? '#00796b' : '#f0f0f0', color: message.role === 'user' ? 'white' : 'black', maxWidth: '80%' }}>
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

          <Box sx={{ padding: '8px', display: 'flex', alignItems: 'center', borderTop: '1px solid #ccc' }}>
            <TextField
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message"
              fullWidth
              size="small"
              sx={{ marginRight: '8px' }}
              disabled={isLoading}
            />
            <IconButton onClick={handleSend} color="primary" disabled={isLoading}>
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      ) : (
        <IconButton onClick={toggleChatbot} sx={{ backgroundColor: '#00796b', color: 'white', width: '50px', height: '50px', borderRadius: '50%', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
          💬
        </IconButton>
      )}
    </Box>
  );
};

export default Chatbot;