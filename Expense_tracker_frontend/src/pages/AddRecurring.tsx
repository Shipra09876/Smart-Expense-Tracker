import { useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";

function AddRecurring() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");
  const [frequency, setFrequency] = useState("monthly");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleSubmit = async (e:any) => {
    e.preventDefault();

    try {
      await ExpenseAPI.post("add_recurring_expense/", {
        name,
        emi_amount: Number(amount),
        frequency,
        start_date: startDate,
        end_date: endDate || null
      });

      navigate("/recurring");
    } catch (err:any) {
      console.log(err.response?.data);
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-3xl mb-6">Add Recurring Expense</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">

        <input placeholder="Name"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setName(e.target.value)} />

        <input type="number" placeholder="Amount"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setAmount(e.target.value)} />

        <select
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setFrequency(e.target.value)}
        >
          <option value="daily">Daily</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>

        <input type="date"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setStartDate(e.target.value)} />

        <input type="date"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setEndDate(e.target.value)} />

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Add EMI
        </button>

      </form>
    </DashboardLayout>
  );
}

export default AddRecurring;