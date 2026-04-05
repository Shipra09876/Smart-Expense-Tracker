import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import AddGoal from "./AddGoal";
import { useNavigate } from "react-router-dom";

function Goals() {
  const [goals, setGoals] = useState<any[]>([]);
  const navigate = useNavigate();

  const fetchGoals = async () => {
    try {
      const res = await ExpenseAPI.get("get_goal/");
      setGoals(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  return (
    <DashboardLayout>
      <h1 className="text-3xl mb-6">Financial Goals</h1>
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => navigate("/add-goal")}
          className="bg-green-600 px-4 py-2 rounded-lg"
        >
          + Add Goals
        </button>
      </div>

      {goals.map((goal) => {
        const progress = (goal.current_balance / goal.target_amount) * 100;

        return (
          <div key={goal.id} className="bg-white/10 p-4 rounded mb-3">
            <p className="font-bold">{goal.name}</p>

            <p>Target: ₹{goal.target_amount}</p>
            <p>Saved: ₹{goal.current_balance}</p>
            <p>Monthly: ₹{goal.monthly_payment}</p>

            <p>Start: {goal.start_date}</p>
            <p>Maturity: {goal.maturity_date}</p>

            <p>Status: {goal.active ? "Active" : "Completed"}</p>

            {/* Progress Bar */}
            <div className="bg-gray-700 h-2 rounded mt-2">
              <div
                className="bg-green-500 h-2 rounded"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        );
      })}
    </DashboardLayout>
  );
}

export default Goals;
