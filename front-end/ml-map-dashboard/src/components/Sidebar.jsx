import { Link } from "react-router-dom";

const Sidebar = () => {
  const menu = [
    { label: "대시보드", path: "/" },
    { label: "재고 관리", path: "/inventory" },
    { label: "재고 현황", path: "/stock-status" },
    { label: "지역 분석", path: "/cluster-analysis" },
    { label: "거래처 관리", path: "/partners" },
    { label: "통계 분석", path: "/statistics" },
    { label: "고용자 관리", path: "/employees" },
  ];

  return (
    <aside className="bg-gray-100 w-48 fixed top-16 left-0 h-[calc(100vh-4rem)] p-4 shadow overflow-y-auto">
      <ul className="space-y-3">
        {menu.map((item, idx) => (
          <li key={idx}>
            <Link
              to={item.path}
              className="hover:text-blue-600 cursor-pointer font-medium block"
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
