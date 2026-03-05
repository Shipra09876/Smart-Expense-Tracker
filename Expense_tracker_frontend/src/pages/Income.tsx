import { useEffect, useState } from "react";
import { ExpenseAPI } from "../Api/axios";
import DashboardLayout from "../layouts/DashboardLayout";

function Income() {
  const [incomes, setIncomes] = useState<any[]>([]);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [search, setSearch] = useState("");

  const fetchIncome = async () => {
    const res = await ExpenseAPI.get(
      `ListIncome/?month=${month}&year=${year}`
    );

    setIncomes(res.data);
  };

  useEffect(() => {
    fetchIncome();
  }, [month]);

  const totalIncome = incomes.reduce(
    (sum, inc) => sum + Number(inc.amount),
    0
  );

  const filteredIncome = incomes.filter((inc) =>
    inc.source.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Income</h1>

        <button className="bg-green-600 px-4 py-2 rounded-lg">
          + Add Income
        </button>
      </div>

      {/* TOTAL INCOME */}
      <div className="bg-white/10 p-6 rounded-xl mb-6">
        <h2 className="text-lg text-gray-300">
          Total Income ({month}/{year})
        </h2>

        <p className="text-3xl font-bold text-green-400">
          ₹{totalIncome}
        </p>
      </div>

      {/* FILTERS */}
      <div className="flex gap-4 mb-6">

        <select
          className="p-2 rounded bg-white/10"
          value={month}
          onChange={(e) => setMonth(Number(e.target.value))}
        >
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i + 1} value={i + 1}>
              Month {i + 1}
            </option>
          ))}
        </select>

        <input
          placeholder="Search source..."
          className="p-2 rounded bg-white/10"
          onChange={(e) => setSearch(e.target.value)}
        />

      </div>

      {/* INCOME LIST */}
      <div className="space-y-3">

        {filteredIncome.map((inc) => (
          <div
            key={inc.id}
            className="bg-white/10 p-4 rounded-lg flex justify-between"
          >
            <div>
              <p className="font-semibold">{inc.source}</p>
              <p className="text-gray-400 text-sm">
                {inc.month}/{inc.year}
              </p>
            </div>

            <p className="text-green-400 font-bold">
              ₹{inc.amount}
            </p>
          </div>
        ))}

      </div>
    </DashboardLayout>
  );
}

export default Income;


// test deploy