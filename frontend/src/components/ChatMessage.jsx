import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';

const ChatMessage = ({ message }) => {
    const { text, isUser, timestamp, error } = message;
    
    return (
        <div className={`message ${isUser ? 'user-message' : 'bot-message'} ${error ? 'error-message' : ''}`}>
            <div className="message-avatar">
                {isUser ? '👤' : '🤖'}
            </div>
            <div className="message-content">
                <div className="message-text">{text}</div>
                <div className="message-timestamp">
                    {formatDistanceToNow(timestamp || new Date(), { 
                        addSuffix: true,
                        locale: es 
                    })}
                </div>
            </div>
        </div>
    );
};

export default ChatMessage; 