import React, { useEffect, useState } from "react";
import axios from 'axios';


function SearchBar() {
    // const [query, setQuery] = useState("")
    const [queryInput, setQueryInput] = useState("hi")
    const [showOutput, setShowOutput] = useState(false)
    const [outputMsg, setOutputMsg] = useState("Hello")
    const baseURL = "http://127.0.0.1:5000/response"
    
    useEffect(() => {
        console.log("queryInput", queryInput);
    },[queryInput])
    
    const queryChanged = (event) =>{
        setQueryInput(event.target.value)
    }
    
    function submitClicked(){
        console.log("curr val", queryInput)
        setShowOutput(true)
        let result = JSON.stringify(fetchOutput())
        console.log("result from backend", result)
        setOutputMsg(result)
    }

    async function fetchOutput(){
        let results = await axios.get(baseURL, { data: {queryInput} })
        return results
    }

    return (
        <div>
            <div class="topnav">
                <a class="active" href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
                <div class="search-container">
                    <form action="/action_page.php">
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