import { ReactNode } from "react";
import { Link, useNavigate } from "react-router-dom";
import {AccountAPI} from "../Api/axios";
import { ExpenseAPI } from "../Api/axios";

type Props = {
  children: ReactNode;
};

function DashboardLayout({ children }: Props) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    const refresh = localStorage.getItem("refresh");

    try {
      await AccountAPI.post("logout/", { refresh });
    } catch (err) {
      console.log(err);
    }

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  return (
    <div className="flex min-h-screen bg-[#0F1115] text-white">
      {/* Sidebar */}
      <div className="w-64 bg-[#111827] p-6 flex flex-col justify-between">
        <div>
          <h2 className="text-xl font-bold mb-8">Expense Tracker</h2>

          <nav className="space-y-4">
            <Link to="/dashboard" className="block hover:text-purple-400">
              Dashboard
            </Link>

            <Link to="/profile" className="block hover:text-purple-400">
              Profile
            </Link>
            <Link to="/change-password" className="block hover:text-purple-400">
              Change Password
            </Link>
            <Link to="/income" className="block py-2 hover:text-purple-400">
              Income
            </Link>
            <Link to="/expenses" className="block py-2 hover:text-purple-400">
              Expenses
            </Link>
            <Link to="/recurring" className="block py-2 hover:text-purple-400">
              EMI
            </Link>
            <Link to="/goals" className="block py-2 hover:text-purple-400">
              FD
            </Link>
            

          </nav>
        </div>

        <button
          onClick={handleLogout}
          className="bg-red-600 px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 p-10">{children}</div>
    </div>
  );
}

export default DashboardLayout;
