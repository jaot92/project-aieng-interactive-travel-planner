import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../App.css';

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;
        
        try {
            const response = await axios.post('http://localhost:8000/chat', { 
                message: input 
            });
            
            setMessages(prev => [
                ...prev,
                { text: input, isUser: true },
                { text: response.data.response, isUser: false }
            ]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [
                ...prev,
                { text: input, isUser: true },
                { text: "Lo siento, hubo un error al procesar tu solicitud", isUser: false }
            ]);
        }
        setInput('');
    };

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, i) => (
                    <div key={i} className={msg.isUser ? 'user' : 'bot'}>
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-area">
                <input 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Escribe tu mensaje..."
                />
                <button onClick={handleSend}>Enviar</button>
            </div>
        </div>
    );
};

export default ChatInterface; 