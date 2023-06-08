import React, { useState } from 'react';
import chatBotIcon from '../assets/chatbot_icon.svg'
import sendIcon from '../assets/send_icon.svg'
import axios from 'axios';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [response, setResponse] = useState("Welcome to Chatur")
    const [queryInput, setQueryInput] = useState("")
    const [queryResponseJson, setQueryResponseJson] = useState([])
    const baseURL = process.env.REACT_APP_BACKEND_URL

    const toggleChatbot = () => {
        setIsOpen(!isOpen);
    };

    const queryChanged = (event) =>{
        setQueryInput(event.target.value)
    }

    async function generateResponse (){
        if(queryInput){
            console.log("Query : ", queryInput)
            let result = await axios.post(baseURL + "/response", { message:queryInput})
            console.log("Response : ", JSON.stringify(result.data))
            updateQueryResponseJson({"Query":queryInput, "Response":result})
            setResponse(result.data)
        }
    }

    async function updateQueryResponseJson(data){
        let cQueryResponseJson = queryResponseJson
        cQueryResponseJson.push(data)
        setQueryResponseJson(cQueryResponseJson)
        console.log(cQueryResponseJson)
    }

    const ChatbotContent = () =>{
        return(
            <div className="chatbot-content">
                <div className="question-response-ui">{queryResponseJson && createDynamicUiArr()}</div>
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

    const createDynamicUiArr = () =>{
        let totalUI = []
        let uiQuestionArrStore = []
        let uiResposeArrStore = []
        console.log("part2", queryResponseJson)
        queryResponseJson?.forEach((element, index) => {
            console.log("element",element)
            uiQuestionArrStore.push(
                <div className='questions'>
                    {element.Query}
                </div>
            )
            uiResposeArrStore.push(
                <div className='responses'>
                    {element.Response.data}
                </div>
                )
            console.log("data onlyy", element.Response.data)
        });
        let uiLength = uiQuestionArrStore.length
        for(let i=0;i<uiLength; i++){
            totalUI.push(uiQuestionArrStore[i])
            totalUI.push(<br></br>)
            totalUI.push(uiResposeArrStore[i])
            totalUI.push(<br></br>)
        }
        console.log("totalUI",totalUI)
        return totalUI
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





