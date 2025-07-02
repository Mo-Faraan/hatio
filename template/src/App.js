import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FormPage from "./pages/FormPage";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Router>
          <Routes>
            <Route path="/" element={<FormPage/>}/>
          </Routes>
        </Router>
      </header>
    </div>
  );
}
export default App;
