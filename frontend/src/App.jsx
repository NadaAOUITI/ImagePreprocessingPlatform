import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./views/pages/Home"; 
import Gallery from "./views/pages/Gallery";
import Processing from "./views/pages/ProcessingWorkspace";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/gallery" element={<Gallery />} />
        <Route path="/processing" element={<Processing />} />      
      </Routes>
    </BrowserRouter>
  );
}

export default App;
