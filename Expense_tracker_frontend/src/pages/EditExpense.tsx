import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate, useParams } from "react-router-dom";

function EditExpense() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringType, setRecurringType] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");

  const [categoryList, setCategoryList] = useState<any[]>([]);
  const [categoryName, setCategoryName] = useState("");

  // ✅ FETCH CATEGORY LIST
  const fetchCategory = async () => {
    try {
      const res = await ExpenseAPI.get("list_category/");
      setCategoryList(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ FETCH EXPENSE
  const fetchExpense = async () => {
    try {
      const res = await ExpenseAPI.get("get_expense/");
      const exp = res.data.find((e: any) => e.id == id);

      if (!exp) return;

      setTitle(exp.title);
      setDescription(exp.description);
      setPaymentMethod(exp.payment_method || "Cash");
      setIsRecurring(exp.is_recurring);
      setRecurringType(exp.recurring_type || "");
      setAmount(exp.expense_amount);
      setDate(exp.expense_date);

      // 🔥 IMPORTANT FIX
      setCategoryName(exp.category || "");
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchExpense();
    fetchCategory();
  }, []);

  // ✅ SUBMIT
  const handleSubmit = async (e: any) => {
    e.preventDefault();

    try {
      await ExpenseAPI.put(`edit_expense/${id}/`, {
        title,
        description,
        expense_amount: Number(amount),
        expense_date: date,
        category_name: categoryName || undefined,
        payment_method: paymentMethod,
        is_recurring: isRecurring,
        recurring_type: isRecurring ? recurringType : null,
      });

      navigate("/expenses");
    } catch (err: any) {
      console.log(err.response?.data);
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-6">Edit Expense</h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-xl space-y-4 max-w-md"
      >
        {/* TITLE */}
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        />

        {/* DESCRIPTION */}
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        />

        {/* AMOUNT */}
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        />

        {/* DATE */}
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        />

        {/* CATEGORY DROPDOWN ✅ */}
        <select
          value={categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        >
          <option value="">Select Category</option>
          {categoryList.map((cat) => (
            <option key={cat.id} value={cat.category_name}>
              {cat.category_name}
            </option>
          ))}
        </select>

        {/* PAYMENT METHOD ✅ */}
        <select
          value={paymentMethod}
          onChange={(e) => setPaymentMethod(e.target.value)}
          className="w-full p-3 bg-black/30 rounded"
        >
          <option value="Cash">Cash</option>
          <option value="UPI">UPI</option>
          <option value="Card">Card</option>
        </select>

        {/* RECURRING */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={isRecurring}
            onChange={(e) => setIsRecurring(e.target.checked)}
          />
          <label>Recurring Expense</label>
        </div>

        {/* RECURRING TYPE */}
        {isRecurring && (
          <select
            value={recurringType}
            onChange={(e) => setRecurringType(e.target.value)}
            className="w-full p-3 bg-black/30 rounded"
          >
            <option value="">Select Type</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        )}

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Update Expense
        </button>
      </form>
    </DashboardLayout>
  );
}

export default EditExpense;