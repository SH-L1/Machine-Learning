import { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import LeafletMap from "./components/LeafletMap";
import ClusterChart from "./components/ClusterChart";

function App() {
  const [clusterId, setClusterId] = useState("");

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 bg-white overflow-y-auto">
          <h2 className="text-2xl font-bold mb-4">📍 지역 군집 분석</h2>

          {/* 지도 */}
          <LeafletMap />
        </main>
      </div>
    </div>
  );
}

export default App;