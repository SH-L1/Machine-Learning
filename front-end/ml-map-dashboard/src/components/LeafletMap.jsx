import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  Circle,
} from "react-leaflet";
import Papa from "papaparse";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const userIcon = new L.Icon({
  iconUrl: require("../assets/marker-icon-red.png"),
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
  shadowSize: [41, 41],
});


// 지도 중심 이동
const FlyToCluster = ({ position }) => {
  const map = useMap();
  useEffect(() => {
    if (position) {
      map.flyTo(position, 15);
    }
  }, [position, map]);
  return null;
};

// 반경 계산 함수 (800m)
const isWithinRadius = (lat1, lng1, lat2, lng2, radius = 800) => {
  const R = 6371000;
  const toRad = (deg) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c <= radius;
};

const LeafletMap = () => {
  const userPos = [37.56034255,126.8523289]; // 100번 클러스터
  const [clusters, setClusters] = useState([]);
  const [selectedCluster, setSelectedCluster] = useState(null);

  useEffect(() => {
  Papa.parse("/cluster.csv", {
    header: true,
    download: true,
    complete: (results) => {
      const excludedClusterIds = ["33", "127", "240", "173", "95", "168"];

      const parsed = results.data
        .filter((row) => row["위도"] && row["경도"])
        .map((row) => ({
          id: row["클러스터"].toString(),
          name: `군집 ${row["클러스터"]}`,
          lat: parseFloat(row["위도"]),
          lng: parseFloat(row["경도"]),
        }))
        .filter(
          (row) =>
            !isNaN(row.lat) &&
            !isNaN(row.lng) &&
            !excludedClusterIds.includes(row.id)
        )
        .filter((row) =>
          isWithinRadius(userPos[0], userPos[1], row.lat, row.lng, 800)
        );

      // ✅ 가장 가까운 군집 찾기
      let closest = null;
      let minDist = Infinity;
      for (const cluster of parsed) {
        const d = getDistance(userPos[0], userPos[1], cluster.lat, cluster.lng);
        if (d < minDist) {
          minDist = d;
          closest = cluster;
        }
      }

      setClusters(parsed);
      if (closest) {
        setSelectedCluster([closest.lat, closest.lng]);
      }
    },
  });
}, []);

  const getDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371000;
  const toRad = (deg) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};


  return (
    <div className="mt-4">
      {/* ✅ 군집 선택 콤보박스 */}
      <div className="mb-3">
        <label className="mr-2 font-medium text-sm text-gray-700 dark:text-gray-200">
          군집 선택:
        </label>
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
          <option value="" disabled>
            군집을 선택하세요
          </option>
          {clusters.map((cluster) => (
            <option key={cluster.id} value={cluster.id}>
              {cluster.name}
            </option>
          ))}
        </select>
      </div>

      {/* ✅ 지도 렌더링 */}
      <div className="rounded shadow" style={{ height: "500px", width: "100%" }}>
        <MapContainer
          center={userPos}
          zoom={15}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* ✅ 현재 위치 마커 */}
          <Marker position={userPos} icon={userIcon}>
            <Popup>📍 현재 위치</Popup>
          </Marker>

          {/* ✅ 필터된 군집 마커 및 원 */}
          {clusters.map((c) => (
            <div key={c.id}>
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

          {/* ✅ 콤보박스 선택 시 중심 이동 */}
          {selectedCluster && <FlyToCluster position={selectedCluster} />}
        </MapContainer>
      </div>
    </div>
  );
};

export default LeafletMap;
