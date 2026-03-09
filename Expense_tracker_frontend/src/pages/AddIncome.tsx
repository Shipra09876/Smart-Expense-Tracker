import { useState } from "react";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";

function AddIncome() {
  const navigate = useNavigate();

  const [amount, setAmount] = useState("");
  const [source, setSource] = useState("");
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    await ExpenseAPI.post("add_income/", {
      amount,
      source,
      month,
      year
    });

    navigate("/income");
  };

  return (
    <DashboardLayout>

      <h1 className="text-3xl font-bold mb-6">Add Income</h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-xl space-y-4 max-w-md"
      >

        <input
          type="number"
          placeholder="Amount"
          className="w-full p-3 rounded bg-black/30"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Source"
          className="w-full p-3 rounded bg-black/30"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        />

        <select
          className="w-full p-3 rounded bg-black/30"
          value={month}
          onChange={(e) => setMonth(Number(e.target.value))}
        >
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i} value={i + 1}>
              Month {i + 1}
            </option>
          ))}
        </select>

        <input
          type="number"
          placeholder="Year"
          className="w-full p-3 rounded bg-black/30"
          value={year}
          onChange={(e) => setYear(Number(e.target.value))}
        />

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Save Income
        </button>

      </form>

    </DashboardLayout>
  );
}

export default AddIncome;