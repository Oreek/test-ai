import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Card } from 'react-bootstrap';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);

  // Initialize SpeechRecognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    // Check if SpeechRecognition is available
    if (SpeechRecognition) {
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US'; // Set language to English (US)
      setRecognition(recognitionInstance);
    } else {
      console.error("Speech Recognition is not supported in this browser.");
    }
  }, []);

  useEffect(() => {
    // Load chat history from localStorage when the component mounts
    const savedMessages = JSON.parse(localStorage.getItem('chatMessages'));
    if (savedMessages) {
      setMessages(savedMessages);
    }
  }, []);

  useEffect(() => {
    // Save chat history to localStorage whenever messages change
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const sendMessage = async (message) => {
    if (message.trim() === '') return;

    const userMessage = { sender: 'User', text: message, timestamp: new Date().toLocaleTimeString() };
    setMessages([...messages, userMessage]);
    setInput('');
    setTyping(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', { prompt: message });
      const botMessage = {
        sender: 'CoolMan',
        text: response.data.response,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prevMessages => [...prevMessages, botMessage]);
      
      // Call text-to-speech for the bot's response
      speakText(response.data.response);
      
    } catch (error) {
      console.error("Error communicating with the chatbot server:", error);
      const errorMessage = { sender: 'CoolMan', text: 'Sorry, there was an error.', timestamp: new Date().toLocaleTimeString() };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setTyping(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage(input);
    }
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const toggleMic = () => {
    if (recognition) {
      if (isMicActive) {
        // Stop mic and send message
        recognition.stop();
        sendMessage(input); // Send the recognized speech as a message
      } else {
        recognition.start();
      }
      setIsMicActive(!isMicActive);
    }
  };

  // Handle speech recognition result
  useEffect(() => {
    if (recognition) {
      recognition.onresult = (event) => {
        const transcript = event.results[event.resultIndex][0].transcript;
        setInput(transcript); // Update input with recognized speech
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
      };
    }
  }, [recognition]);

  // Text-to-Speech function for bot's reply
  const speakText = (text) => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-US'; // Set language for speech
    window.speechSynthesis.speak(speech); // Speak the text
  };

  return (
    <Container fluid className={`d-flex align-items-center justify-content-center vh-100 ${darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`}>
      <Row className="w-100" style={{ maxWidth: '600px' }}>
        <Col>
          <Card style={{ height: '80vh', backgroundColor: darkMode ? '#2c2c2c' : 'white' }}>
            <Card.Header className={`d-flex justify-content-between align-items-center ${darkMode ? 'bg-secondary' : 'bg-primary text-white'}`}>
              <span>CoolMan Chatbot</span>
              <Form.Check
                type="switch"
                id="dark-mode-switch"
                label={darkMode ? "Light Mode" : "Dark Mode"}
                checked={darkMode}
                onChange={toggleDarkMode}
                className="text-light"
              />
            </Card.Header>
            <Card.Body className="p-3 d-flex flex-column" style={{ overflowY: 'auto' }}>
              {messages.map((msg, index) => (
                <div key={index} className={`d-flex mb-3 ${msg.sender === 'User' ? 'justify-content-end' : ''}`}>
                  <div className={`p-2 rounded ${msg.sender === 'User' ? 'bg-primary text-white' : darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`} style={{ maxWidth: '75%' }}>
                    <strong>{msg.sender}:</strong> {msg.text}
                    <div className="text-muted small text-right">{msg.timestamp}</div>
                  </div>
                </div>
              ))}
              {typing && (
                <div className="d-flex mb-3">
                  <div className={`p-2 rounded ${darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`} style={{ maxWidth: '75%' }}>
                    <strong>CoolMan:</strong> Typing...
                  </div>
                </div>
              )}
            </Card.Body>
            <Card.Footer className="p-2">
              <Form onSubmit={(e) => { e.preventDefault(); sendMessage(input); }}>
                <Row>
                  <Col xs={9}>
                    <Form.Control
                      type="text"
                      placeholder="Type your message..."
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      className={darkMode ? 'bg-dark text-white' : ''}
                    />
                  </Col>
                  <Col xs={3} className="d-grid">
                    <Button variant={darkMode ? 'secondary' : 'primary'} onClick={() => sendMessage(input)}>
                      Send
                    </Button>
                  </Col>
                </Row>
              </Form>
              <Button variant={isMicActive ? 'danger' : 'success'} onClick={toggleMic} className="mt-2 w-100">
                {isMicActive ? 'Stop Mic' : 'Start Mic'}
              </Button>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default App;






// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';
// import 'bootstrap/dist/css/bootstrap.min.css';

// function App() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState('');

//   // Function to send message to the backend
//   const sendMessage = async () => {
//     if (input.trim() === '') return;

//     const userMessage = { sender: 'User', text: input };
//     setMessages([...messages, userMessage]);
//     setInput('');

//     try {
//       const response = await axios.post('http://127.0.0.1:5000/chat', { prompt: input });
//       const botMessage = { sender: 'CoolMan', text: response.data.response };
//       setMessages(prevMessages => [...prevMessages, botMessage]);
//     } catch (error) {
//       console.error("Error communicating with the chatbot server:", error);
//       const errorMessage = { sender: 'CoolMan', text: 'Sorry, there was an error.' };
//       setMessages(prevMessages => [...prevMessages, errorMessage]);
//     }
//   };

//   // Function to handle user input change
//   const handleInputChange = (event) => {
//     setInput(event.target.value);
//   };

//   // Function to handle "Enter" key press
//   const handleKeyPress = (event) => {
//     if (event.key === 'Enter') {
//       sendMessage();
//     }
//   };

//   return (
//     <div className="App">
//       <div className="chat-container">
//         <div className="chat-box">
//           {messages.map((message, index) => (
//             <div key={index} className={`message ${message.sender === 'User' ? 'user-message' : 'bot-message'}`}>
//               <strong>{message.sender}:</strong> {message.text}
//             </div>
//           ))}
//         </div>
//         <div className="input-container">
//           <input
//             type="text"
//             value={input}
//             onChange={handleInputChange}
//             onKeyPress={handleKeyPress}
//             placeholder="Type a message..."
//           />
//           <button onClick={sendMessage}>Send</button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;
