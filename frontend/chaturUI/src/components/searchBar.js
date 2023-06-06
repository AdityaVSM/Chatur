import React, { useEffect, useState } from "react";
import axios from 'axios';


function SearchBar() {
    // const [query, setQuery] = useState("")
    const [queryInput, setQueryInput] = useState("hi")
    const [showOutput, setShowOutput] = useState(false)
    const [outputMsg, setOutputMsg] = useState("Hello")
    const baseURL = "http://localhost:5000/response"
    
    
    const queryChanged = (event) =>{
        setQueryInput(event.target.value)
    }
    
    async function submitClicked(){
        console.log("Query : ", queryInput)
        setShowOutput(true)
        let result = await axios.post(baseURL, { message:queryInput})
        console.log("Response : ", JSON.stringify(result.data))
        setOutputMsg(result.data)
    }


    return (
        <div>
            <div class="topnav">
                <a class="active" href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
                <div class="search-container">
                    <form >
                    <input 
                        type="text" 
                        placeholder="Search.." 
                        name="search"
                        onChange={(e) => {queryChanged(e);}}
                    />
                    <button 
                        type="button"
                        onClick={submitClicked}>
                        Submit
                    </button>
                    </form>
                </div>
            </div>

            {showOutput && 
                    <p>
                        {outputMsg}
                    </p>
            }
        </div>
        
    )
    
}
export default SearchBar;