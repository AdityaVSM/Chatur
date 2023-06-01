import './App.css';
import Chatbot from './components/ChatBotContainer';
import SearchBar from './components/searchBar';


function App() {
  return (
    <div>
      <div>
        <SearchBar/>
      </div>
      <div>
        <Chatbot/>
      </div>
    </div>
  );
}
export default App;
