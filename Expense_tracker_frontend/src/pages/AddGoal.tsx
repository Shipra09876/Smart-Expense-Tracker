import { useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";

function AddGoal() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [target, setTarget] = useState("");
  const [monthly, setMonthly] = useState("");
  const [startDate, setStartDate] = useState("");

  const handleSubmit = async (e:any) => {
    e.preventDefault();

    try {
      await ExpenseAPI.post("add_goal/", {
        name,
        target_amount: Number(target),
        monthly_payment: Number(monthly),
        current_balance: 0,
        start_date: startDate
      });

      navigate("/goals");
    } catch (err:any) {
      console.log(err.response?.data);
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-3xl mb-6">Add Goal</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">

        <input placeholder="Goal Name"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setName(e.target.value)} />

        <input type="number" placeholder="Target Amount"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setTarget(e.target.value)} />

        <input type="number" placeholder="Monthly Saving"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setMonthly(e.target.value)} />

        <input type="date"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e)=>setStartDate(e.target.value)} />

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Add Goal
        </button>

      </form>
    </DashboardLayout>
  );
}

export default AddGoal;