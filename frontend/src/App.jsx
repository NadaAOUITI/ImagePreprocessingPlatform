import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./views/pages/Home"; 
import Gallery from "./views/pages/Gallery";
import Processing from "./views/pages/ProcessingWorkspace";
import HistogramPage from "./views/pages/HistogramPage"; 
import ImageHistoryPage from "./views/pages/ImageHistoryPage";
import ErrorPage from "./views/pages/ErrorPage"; 
import BlurFilters from "./views/pages/BlurFilters";
import EdgeFilters from "./views/pages/EdgeFilters";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/gallery" element={<Gallery />} />
        <Route path="/processing" element={<Processing />} />  
        <Route path="/histogram" element={<HistogramPage />} /> 
        <Route path="/historique" element={<ImageHistoryPage />} /> 
        <Route path="/blur-filters" element={<BlurFilters />} /> 
          <Route path="/edge-filters" element={<EdgeFilters />} /> 
        <Route path="*" element={<ErrorPage message="Page introuvable." />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
