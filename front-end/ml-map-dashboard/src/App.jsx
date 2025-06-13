import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import LeafletMap from "./components/LeafletMap";
import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import StockStatus from "./pages/StockStatus";
import ClusterAnalysis from "./pages/ClusterAnalysis";
import Partners from "./pages/Partners";
import Statistics from "./pages/Statistics";
import Employees from "./pages/Employees";

function App() {
  const [clusterId, setClusterId] = useState("");

  return (
    <Router>
      <div className="h-screen flex flex-col">
        <Header />
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1 p-6 bg-white overflow-y-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/inventory" element={<Inventory />} />
                <Route path="/" element={<Dashboard />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/stock-status" element={<StockStatus />} />
              <Route path="/cluster-analysis" element={<ClusterAnalysis />} />
              <Route path="/partners" element={<Partners />} />
              <Route path="/statistics" element={<Statistics />} />
              <Route path="/employees" element={<Employees />} />
              <Route
                path="/cluster-analysis"
                element={
                  <>
                    <h2 className="text-2xl font-bold mb-4">📍 지역 군집 분석</h2>
                    <LeafletMap />
                  </>
                }
              />
              {/* 다른 경로들도 여기에 추가 */}
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
