import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  Circle
} from "react-leaflet";
import Papa from "papaparse";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

// 지도 중심을 이동시키는 컴포넌트
const FlyToCluster = ({ position }) => {
  const map = useMap();
  useEffect(() => {
    if (position) {
      map.flyTo(position, 15);
    }
  }, [position, map]);
  return null;
};

const LeafletMap = () => {
  const [clusters, setClusters] = useState([]);
  const [currentPos, setCurrentPos] = useState(null);
  const [selectedCluster, setSelectedCluster] = useState(null);

  useEffect(() => {
    Papa.parse("/cluster.csv", {
  header: true,
  download: true,
  complete: (results) => {
    const parsed = results.data
      .filter((row) => row["위도"] && row["경도"]) // 빈 값 제거
      .map((row) => ({
        id: row["클러스터"],
        name: `군집 ${row["클러스터"]}`,
        lat: parseFloat(row["위도"]),
        lng: parseFloat(row["경도"]),
      }))
      .filter((row) => !isNaN(row.lat) && !isNaN(row.lng)); // NaN 제거

    setClusters(parsed);
  },
});


    // ✅ 현재 위치 가져오기
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setCurrentPos([latitude, longitude]);
        },
        () => {
          setCurrentPos([37.5665, 126.9780]); // fallback: 서울시청
        }
      );
    }
  }, []);

  return (
    <div className="mt-4">

          {/* ✅ 군집 선택 콤보박스 */}
    <div className="mb-3">
      <label className="mr-2 font-medium text-sm text-gray-700">군집 선택:</label>
      <select
        className="border border-gray-300 rounded px-2 py-1 text-sm"
        onChange={(e) => {
          const selected = clusters.find((c) => c.id === e.target.value);
          if (selected) {
            setSelectedCluster([selected.lat, selected.lng]);
          }
        }}
        defaultValue=""
      >
        <option value="" disabled>군집을 선택하세요</option>
        {clusters.map((cluster) => (
          <option key={cluster.id} value={cluster.id}>
            {cluster.name}
          </option>
        ))}
      </select>
    </div>


      <div className="rounded shadow" style={{ height: "500px", width: "100%" }}>
        {currentPos && (
          <MapContainer
            center={currentPos}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* ✅ 현재 위치 */}
            <Marker position={currentPos}>
              <Popup>📍 현재 위치</Popup>
            </Marker>

            {/* ✅ 클러스터 마커 + 원 */}
            {clusters.map((c) => (
              <div key={c.id}>
                <Marker position={[c.lat, c.lng]}>
                  <Popup>{c.name}</Popup>
                </Marker>
                <Circle
                  center={[c.lat, c.lng]}
                  radius={800}
                  pathOptions={{
                    color: "blue",
                    fillColor: "blue",
                    fillOpacity: 0.25,
                  }}
                />
              </div>
            ))}

            {/* ✅ 선택된 군집으로 이동 */}
            {selectedCluster && <FlyToCluster position={selectedCluster} />}
          </MapContainer>
        )}
      </div>
    </div>
  );
};

export default LeafletMap;
