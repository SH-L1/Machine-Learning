const Sidebar = () => {
  const menu = [
    "대시보드", "재고 관리", "재고 현황", "지역 분석",
    "거래처 관리", "통계 분석", "고용자 관리"
  ];

  return (
    <aside className="bg-gray-100 w-48 h-full p-4 shadow">
      <ul className="space-y-3">
        {menu.map((item, idx) => (
          <li key={idx} className="hover:text-blue-600 cursor-pointer font-medium">
            {item}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
