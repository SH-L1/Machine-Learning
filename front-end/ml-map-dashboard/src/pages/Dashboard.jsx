import LeafletMap from "../components/LeafletMap";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

const Dashboard = () => {
  // 1. 요약 지표 데이터
  const stats = [
    { label: "전체 재고", value: 1280, icon: "📦" },
    { label: "거래처", value: 45, icon: "🤝" },
    { label: "입출고 건수", value: 192, icon: "🚚" },
    { label: "직원 수", value: 12, icon: "👨‍💼" },
  ];

  // 2. 최근 입출고 내역 데이터
  const recentLogs = [
    { item: "A형 건전지", type: "입고", quantity: 100, date: "2025-06-13", manager: "홍길동" },
    { item: "B형 건전지", type: "출고", quantity: 50, date: "2025-06-12", manager: "김철수" },
    { item: "충전 케이블", type: "입고", quantity: 80, date: "2025-06-11", manager: "이영희" },
    { item: "무선 마우스", type: "출고", quantity: 20, date: "2025-06-10", manager: "박지민" },
    { item: "USB 허브", type: "입고", quantity: 40, date: "2025-06-09", manager: "최수정" },
  ];

  // 3. 월별 입출고 데이터
  const monthlyFlow = [
    { month: "1월", inbound: 120, outbound: 80 },
    { month: "2월", inbound: 150, outbound: 100 },
    { month: "3월", inbound: 130, outbound: 90 },
    { month: "4월", inbound: 170, outbound: 110 },
    { month: "5월", inbound: 160, outbound: 95 },
    { month: "6월", inbound: 180, outbound: 120 },
  ];

  // 4. 공지사항 데이터
  const notifications = [
    { message: "수요일에 제고를 좀더 쌓아두시는걸 추천." },
    { message: "수요일에 인력을 늘리시는걸 추천." },
    { message: "60대 이상 손님들이 좋아할만한 메뉴 개발, 이벤트 시행." },
  ];



  return (
    <div className="space-y-10">
      <h2 className="text-2xl font-bold">📊 대시보드</h2>

      {/* 요약 카드 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div
            key={idx}
            className="bg-white border rounded-2xl shadow p-4 flex items-center space-x-4"
          >
            <div className="text-3xl">{stat.icon}</div>
            <div>
              <p className="text-sm text-gray-500">{stat.label}</p>
              <p className="text-xl font-semibold">{stat.value.toLocaleString()}</p>
            </div>
          </div>
        ))}
      </div>

      {/* 인사이트 영역 */}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="text-xl font-semibold mb-4">📢 인사이트</h3>
        <ul className="space-y-2 text-sm">
          {notifications.map((note, idx) => (
            <li key={idx} className="flex justify-between border-b pb-1">
              <span className="text-gray-800">{note.message}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 최근 입출고 테이블 */}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="text-xl font-semibold mb-4">📑 최근 입출고 현황</h3>
        <table className="min-w-full text-sm">
          <thead className="text-left border-b">
            <tr>
              <th className="py-2 px-3">품목명</th>
              <th className="py-2 px-3">구분</th>
              <th className="py-2 px-3">수량</th>
              <th className="py-2 px-3">날짜</th>
              <th className="py-2 px-3">담당자</th>
            </tr>
          </thead>
          <tbody>
            {recentLogs.map((log, idx) => (
              <tr key={idx} className="border-b hover:bg-gray-50">
                <td className="py-2 px-3">{log.item}</td>
                <td className="py-2 px-3">{log.type}</td>
                <td className="py-2 px-3">{log.quantity}</td>
                <td className="py-2 px-3">{log.date}</td>
                <td className="py-2 px-3">{log.manager}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 월별 입출고 라인 차트 */}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="text-xl font-semibold mb-4">📈 월별 입출고 건수</h3>
        <div className="w-full h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={monthlyFlow} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="inbound" name="입고" stroke="#8884d8" />
              <Line type="monotone" dataKey="outbound" name="출고" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 지역 군집 지도 */}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="text-xl font-semibold mb-4">🗺️ 주요 군집 지역</h3>
        <div className="w-full h-96 rounded overflow-hidden">
          <LeafletMap />
        </div>
      </div>

      {/*그래프 시각화*/}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="text-xl font-semibold mb-4">📊 상관계수 그래프</h3>
        <div className="w-full h-96">
          <img src="/CorrelationData.png" alt="상관계수 그래프" className="w-full" />
        </div>
      </div>

      <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="text-xl font-semibold mb-4">📈 변수 중요도 상위 30개</h3>
      <div className="w-full overflow-auto">
        <img src="/importance_top30.png" alt="상위 30개 변수 중요도" className="w-full" />
      </div>
    </div>

    </div>
  );
};

export default Dashboard;
