const Header = ({ toggleDarkMode }) => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-blue-600 text-white px-6 py-3 flex justify-between items-center shadow">
      <h1 className="text-xl font-bold">재고관리 시스템</h1>
      <div>
        <button className="bg-blue-500 hover:bg-blue-400 px-3 py-1 rounded text-sm">대시보드</button>
        <button
          className="ml-2 bg-blue-500 hover:bg-blue-400 px-3 py-1 rounded text-sm"
          onClick={toggleDarkMode}
        >
          설정
        </button>
      </div>
    </header>
  );
};

export default Header;
