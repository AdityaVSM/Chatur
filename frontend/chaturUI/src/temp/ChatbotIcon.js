import React, { useState } from 'react';
import './ChatbotIcon.css';

const ChatbotIcon = ({ onToggle }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChatbox = () => {
    setIsOpen(!isOpen);
    onToggle(!isOpen); // Notify parent component about the state change
  };

  return (
    <>
      {isOpen ? (
        <div className="chatbox-icon open" onClick={toggleChatbox}>
          <span className="icon-close">X</span>
        </div>
      ) : (
        <div className="chatbox-icon closed" onClick={toggleChatbox}>
          <span className="icon">&#128172;</span>
        </div>
      )}
    </>
  );
};

export default ChatbotIcon;
