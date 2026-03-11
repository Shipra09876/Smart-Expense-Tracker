import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";

function EditIncome() {

  const { id } = useParams();
  const navigate = useNavigate();

  const [amount, setAmount] = useState("");
  const [source, setSource] = useState("");
  const [month, setMonth] = useState(1);
  const [year, setYear] = useState(new Date().getFullYear());

  const fetchIncome = async () => {

    const res = await ExpenseAPI.get(`ListIncome/${id}/`);

    setAmount(res.data.amount);
    setSource(res.data.source);
    setMonth(res.data.month);
    setYear(res.data.year);
  };

  useEffect(() => {
    fetchIncome();
  }, []);

  const handleSubmit = async (e:any) => {

    e.preventDefault();

    await ExpenseAPI.put(
      `edit_income/${id}/`,
      {
        amount,
        source,
        month,
        year
      }
    );

    navigate("/income");
  };

  return (
    <DashboardLayout>

      <h1 className="text-3xl font-bold mb-6">
        Edit Income
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-xl space-y-4 max-w-md"
      >

        <input
          type="number"
          value={amount}
          onChange={(e)=>setAmount(e.target.value)}
          className="w-full p-3 rounded bg-black/30"
        />

        <input
          type="text"
          value={source}
          onChange={(e)=>setSource(e.target.value)}
          className="w-full p-3 rounded bg-black/30"
        />

        <select
          value={month}
          onChange={(e)=>setMonth(Number(e.target.value))}
          className="w-full p-3 rounded bg-black/30"
        >
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i} value={i+1}>
              Month {i+1}
            </option>
          ))}
        </select>

        <input
          type="number"
          value={year}
          onChange={(e)=>setYear(Number(e.target.value))}
          className="w-full p-3 rounded bg-black/30"
        />

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Update Income
        </button>

      </form>

    </DashboardLayout>
  );
}

export default EditIncome;