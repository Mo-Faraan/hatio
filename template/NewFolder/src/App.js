import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Form from "./components/Form";
import Validate from "./components/Validate";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Router>
          <Routes>
            <Route path="/" element={<Form/>}/>
            <Route path="/jsonvalidation" element={<Validate/>}/>
          </Routes>
        </Router>
      </header>
    </div>
  );
}

export default App;
