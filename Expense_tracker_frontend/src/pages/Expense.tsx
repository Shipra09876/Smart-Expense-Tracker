import { useEffect, useState } from "react";
import { ExpenseAPI } from "../Api/axios";
import DashboardLayout from "../layouts/DashboardLayout";

function Expense() {
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");
  const [category_name, setCategory] = useState("");
  const [expenses, setExpenses] = useState<any[]>([]);

  const inputStyle =
    "w-full p-2 rounded-lg bg-white/10 text-white outline-none";

  const fetchExpenses = async () => {
    const res = await ExpenseAPI.get("get_expense/");
    setExpenses(res.data);
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    await ExpenseAPI.post("add_expense/", {
      title,
      expense_amount: amount,
      expense_date: date,
      category_name,
    });

    alert("Expense Added 💸");
    fetchExpenses();
  };

  const deleteExpense = async (id: number) => {
    await ExpenseAPI.delete(`delete_expense/${id}/`);
    fetchExpenses();
  };

  return (
    <DashboardLayout>
      <h1 className="text-3xl mb-6">Expenses</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
        <input
          placeholder="Title"
          className={inputStyle}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          type="number"
          placeholder="Amount"
          className={inputStyle}
          onChange={(e) => setAmount(e.target.value)}
        />

        <input
          type="date"
          className={inputStyle}
          onChange={(e) => setDate(e.target.value)}
        />

        <input
          placeholder="Category"
          className={inputStyle}
          onChange={(e) => setCategory(e.target.value)}
        />

        <button className="bg-red-600 px-4 py-2 rounded-lg">
          Add Expense
        </button>
      </form>

      <div className="mt-10">
        {expenses.map((exp) => (
          <div
            key={exp.id}
            className="bg-white/10 p-3 rounded-lg mb-2 flex justify-between"
          >
            <span>
              {exp.title} - ₹{exp.expense_amount}
            </span>

            <button
              onClick={() => deleteExpense(exp.id)}
              className="text-red-400"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}

export default Expense;