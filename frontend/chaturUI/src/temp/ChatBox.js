import './Chatbox.css';
import React, { useState } from 'react';
import axios from 'axios';
import chatBotIcon from '../assets/chatbot_icon.svg'


const Chatbox = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [response, setResponse] = useState("Welcome to Chatur")
    const [queryInput, setQueryInput] = useState("")
    const [queryResponseJson, setQueryResponseJson] = useState([])
    // const baseURL = process.env.REACT_APP_BACKEND_URL
    const baseURL = "http://127.0.0.1:5000"

    const toggleChatbot = () => {
        setIsOpen(!isOpen);
    };

    const queryChanged = (event) =>{
        setQueryInput(event.target.value)
    }
    
    function getCorrectDataFromResponse(result){
        switch (result.data.code) {
            case 0 : return result.data.response_message;
            case 1 : return "\nName: "+result.data.name + "         \nEmail:"+ result.data.email + (result.data.url ? ("   url: "+result.data.url) : " ");
            case 2 : return result.data.fee + (result.data.url ? (" url: "+result.data.url) : " ");
            case 3 : return result.data.name + "Location: " + result.data.location + (result.data.url ? (" url: "+result.data.url) : " ");
            default : return "Not able to process this query for now";
        }
    }

    async function generateResponse (){
        if(queryInput){
            console.log("Query : ", queryInput)
            let result = await axios.post(baseURL + "/response", { message:queryInput})
            // console.log("Response : ", result)
            let final_result = getCorrectDataFromResponse(result)
            console.log("mann",final_result)
            updateQueryResponseJson({"Query":queryInput, "Response":final_result})
            setResponse(final_result)
        }
    }
    
    async function updateQueryResponseJson(data){
        let cQueryResponseJson = queryResponseJson
        cQueryResponseJson.push(data)
        setQueryResponseJson(cQueryResponseJson)
        // console.log(cQueryResponseJson)
    }
    
    const createDynamicUiArr = () =>{
        let totalUI = []
        let uiQuestionArrStore = []
        let uiResposeArrStore = []
        // console.log("part2", queryResponseJson)
        queryResponseJson?.forEach((element, index) => {
            // console.log("element",element)
            uiQuestionArrStore.push(
                <Message content={element.Query} isUser={true} />
            )
            let responseArr = element.Response.split(' ')
            if(responseArr.indexOf('url:') != -1){
                // let displayResponseWithoutUrl = ''.join(responseArr)
                uiResposeArrStore.push(
                    <Message 
                        content={
                            <span>
                                {element.Response}
                                <a target='_blank' href={responseArr[responseArr.indexOf('url:')+1]}>
                                    {" click here"}
                                </a>
                            </span>                            
                            } 
                        isUser={false} />
                    )
            }else{
                uiResposeArrStore.push(
                    <Message 
                        content={element.Response} 
                        isUser={false} />
                    )
            }
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
    

    const Message = ({ content, isUser }) => {
        return (
            <div 
                className={`message ${isUser ? 'user' : 'bot'}`}>
                <span className="content">{content}</span>
            </div>
        );
    };    


    return (
        <div>
            {isOpen && (
                <div className="chatbox-container">
                    <div className="chatbox-header">
                        <span>Chatur</span>
                    </div>
                    <div className="chatbox-body">
                        {queryResponseJson && createDynamicUiArr()}
                    </div>
                    <div className="chatbox-footer">
                        <input 
                            type="text" 
                            placeholder="Type your message..." 
                            onChange={(e) => {setQueryInput(e.target.value)}}
                        />
                        <button onClick={generateResponse}>Send</button>
                    </div>
                    
                </div>
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

export default Chatbox;
