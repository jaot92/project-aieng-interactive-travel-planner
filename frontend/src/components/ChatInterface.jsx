import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import '../App.css';

const ChatInterface = () => {
    const [messages, setMessages] = useState(() => {
        const saved = localStorage.getItem('chatHistory');
        return saved ? JSON.parse(saved) : [];
    });
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Persistir mensajes en localStorage
    useEffect(() => {
        localStorage.setItem('chatHistory', JSON.stringify(messages));
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;
        
        const userMessage = {
            text: input,
            isUser: true,
            timestamp: new Date(),
        };
        
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        
        try {
            const response = await axios.post('http://localhost:8000/chat', { 
                message: input 
            });
            
            const botMessage = {
                text: response.data.response,
                isUser: false,
                timestamp: new Date(),
            };
            
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
            const errorMessage = {
                text: "Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.",
                isUser: false,
                timestamp: new Date(),
                error: true
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const clearHistory = () => {
        if (window.confirm('¿Estás seguro de que quieres borrar todo el historial del chat?')) {
            setMessages([]);
            localStorage.removeItem('chatHistory');
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h2>The Hitchhiker's Guide to Puerto Rico 🇵🇷</h2>
                <button onClick={clearHistory} className="clear-button">
                    Borrar historial
                </button>
            </div>
            
            <div className="messages">
                {messages.map((msg, i) => (
                    <ChatMessage key={i} message={msg} />
                ))}
                {isLoading && (
                    <div className="loading-message">
                        <div className="loading-dots">
                            <span>.</span><span>.</span><span>.</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            
            <div className="input-area">
                <input 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Escribe tu mensaje..."
                    disabled={isLoading}
                />
                <button 
                    onClick={handleSend} 
                    disabled={isLoading || !input.trim()}
                    className={isLoading ? 'loading' : ''}
                >
                    {isLoading ? 'Enviando...' : 'Enviar'}
                </button>
            </div>
        </div>
    );
};

export default ChatInterface; 