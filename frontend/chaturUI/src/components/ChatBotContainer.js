import React, { useState } from 'react';
import chatBotIcon from '../assets/chatbot_icon.svg'
import sendIcon from '../assets/send_icon.svg'
import axios from 'axios';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [response, setResponse] = useState("Welcome to Chatur")
    const [queryInput, setQueryInput] = useState("")
    const baseURL = "http://localhost:5000/response"

    const toggleChatbot = () => {
        setIsOpen(!isOpen);
    };

    const queryChanged = (event) =>{
        setQueryInput(event.target.value)
    }

    async function generateResponse (){
        console.log("Query : ", queryInput)
        let result = await axios.post(baseURL, { message:queryInput})
        console.log("Response : ", JSON.stringify(result.data))
        setResponse(result.data)
    }

    const ChatbotContent = () =>{
        return(
            <div className="chatbot-content">
                <h3>{response}</h3>
                <div className='query-box'>
                        <input 
                            value={queryInput}
                            type="text" 
                            name="search"
                            autoFocus
                            onChange={(e) => {setQueryInput(e.target.value)}}
                        />
                    <img 
                        src={sendIcon} 
                        alt='send icon' 
                        onClick={generateResponse}
                    />
                </div>
                
            </div>
        )
    }

    return (
        <div >
            {isOpen && (
                <ChatbotContent/>
            )}

            <div className="floating-icon" onClick={toggleChatbot}>
                <img 
                    src={chatBotIcon} 
                    alt="Floating Icon" 
                />
        </div>
        </div>
    );
};

export default Chatbot;





