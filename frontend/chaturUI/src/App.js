import './App.css';
import Chatbot from './components/ChatBotContainer';
import SearchBar from './components/searchBar';
import Chatbox from './temp/ChatBox';
import ChatbotIcon from './temp/ChatbotIcon';
import Body from './temp/Body';
import React, { useState } from 'react';



function App() {

  return (
    <div className="App">
        <SearchBar/>
        <Body/>
        <Chatbox/>
    </div>
  );
}
export default App;
