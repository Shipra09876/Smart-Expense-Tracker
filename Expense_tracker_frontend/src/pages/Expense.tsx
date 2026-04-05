import { useEffect, useState } from "react";
import { ExpenseAPI } from "../Api/axios";
import DashboardLayout from "../layouts/DashboardLayout";
import { useNavigate } from "react-router-dom";
import { FaEdit, FaTrash } from "react-icons/fa";

function Expenses() {
  const navigate = useNavigate();

  const [expenses, setExpenses] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  const fetchExpenses = async () => {
    try {
      const res = await ExpenseAPI.get("get_expense/", {
        params: {
          search,
          category: categoryFilter,
        },
      });

      console.log(res.data);
      setExpenses(res.data);
    } catch (err: any) {
      console.log(err.response?.data);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, [search, categoryFilter]);

  const totalExpense = expenses.reduce(
    (sum, e) => sum + Number(e.expense_amount),
    0
  );

  const deleteExpense = async (id: number) => {
    if (!window.confirm("Delete this expense?")) return;

    try {
      await ExpenseAPI.delete(`delete_expense/${id}/`);
      fetchExpenses();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <DashboardLayout>
      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Expenses</h1>

        <button
          onClick={() => navigate("/add-expense")}
          className="bg-green-600 px-4 py-2 rounded-lg"
        >
          + Add Expense
        </button>
      </div>

      {/* TOTAL */}
      <div className="bg-white/10 p-6 rounded-xl mb-6">
        <h2 className="text-gray-300">Total Expense</h2>
        <p className="text-3xl font-bold text-red-400">
          ₹{totalExpense}
        </p>
      </div>

      {/* FILTERS */}
      <div className="flex gap-4 mb-6">
        <input
          placeholder="Search title..."
          className="p-2 rounded bg-white/10"
          onChange={(e) => setSearch(e.target.value)}
        />

        <input
          placeholder="Category..."
          className="p-2 rounded bg-white/10"
          onChange={(e) => setCategoryFilter(e.target.value)}
        />
      </div>

      {/* LIST */}
      <div className="space-y-3">
        {expenses.length === 0 ? (
          <p className="text-gray-400">No expenses found</p>
        ) : (
          expenses.map((exp) => (
            <div
              key={exp.id}
              className="bg-white/10 p-4 rounded-lg flex justify-between items-center"
            >
              <div>
                <p className="font-semibold">{exp.title}</p>
                <p className="text-gray-400 text-sm">
                  {exp.expense_date}
                </p>
                <p className="text-gray-500 text-sm">
                  {exp.category_name || "No Category"}
                </p>
              </div>

              <div className="flex items-center gap-4">
                <p className="text-red-400 font-bold">
                  ₹{exp.expense_amount}
                </p>

                <FaEdit
                  className="cursor-pointer"
                  onClick={() =>
                    navigate(`/edit-expense/${exp.id}`)
                  }
                />

                <FaTrash
                  className="cursor-pointer text-red-500"
                  onClick={() => deleteExpense(exp.id)}
                />
              </div>
            </div>
          ))
        )}
      </div>
    </DashboardLayout>
  );
}

export default Expenses;