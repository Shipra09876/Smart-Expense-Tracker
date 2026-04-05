import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";

function Recurring() {
  const navigate = useNavigate();
  const [emis, setEmis] = useState<any[]>([]);

  const fetchEMI = async () => {
    try {
      const res = await ExpenseAPI.get("get_recurring_expense/");
      setEmis(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchEMI();
  }, []);

  return (
    <DashboardLayout>
      <h1 className="text-3xl mb-6">Recurring Expenses</h1>

      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => navigate("/add-recurring")}
          className="bg-green-600 px-4 py-2 rounded-lg"
        >
          + Add EMI
        </button>
      </div>

      {emis.length === 0 ? (
        <p>No EMI found</p>
      ) : (
        emis.map((emi) => (
          <div key={emi.id} className="bg-white/10 p-4 rounded mb-3">
            <p className="font-bold">{emi.name}</p>
            <p>₹{emi.emi_amount}</p>
            <p>Frequency: {emi.frequency}</p>
            <p>Start: {emi.start_date}</p>
            <p>End: {emi.end_date || "No End"}</p>
            <p>Next Due: {emi.next_due_date}</p>
            <p>Status: {emi.active ? "Active" : "Stopped"}</p>
          </div>
        ))
      )}
    </DashboardLayout>
  );
}

export default Recurring;
