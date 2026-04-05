import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { ExpenseAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";

function AddExpense() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");
  const [description, setDescription] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringType, setRecurringType] = useState("");

  const [categoryList, setCategoryList] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [newCategory, setNewCategory] = useState("");

  const fetchCategory = async () => {
    try {
      const res = await ExpenseAPI.get("list_category/");
      setCategoryList(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCategory();
  }, []);

  const addCategory = async () => {
    if (!newCategory) return;

    try {
      await ExpenseAPI.post("add_category/", {
        category_name: newCategory,
      });

      setSelectedCategory(newCategory); // auto select
      setNewCategory("");
      fetchCategory();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    try {
      await ExpenseAPI.post("add_expense/", {
        title,
        description,
        expense_amount: Number(amount),
        expense_date: date,
        category_name: selectedCategory,
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
      <h1 className="text-3xl font-bold mb-6">Add Expense</h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-6 rounded-xl space-y-4 max-w-md"
      >
        <input
          placeholder="Title"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          placeholder="Description"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e) => setDescription(e.target.value)}
        />

        <input
          type="number"
          placeholder="Amount"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e) => setAmount(e.target.value)}
        />

        <input
          type="date"
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e) => setDate(e.target.value)}
        />

        <select
          className="w-full p-3 bg-black/30 rounded"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">Select Category</option>

          {categoryList.map((cat) => (
            <option key={cat.id} value={cat.category_name}>
              {cat.category_name}
            </option>
          ))}
        </select>

        <div className="flex gap-2">
          <input
            placeholder="New Category"
            value={newCategory}
            className="w-full p-3 bg-black/30 rounded"
            onChange={(e) => setNewCategory(e.target.value)}
          />

          <button
            type="button"
            onClick={addCategory}
            className="bg-blue-600 px-4 rounded"
          >
            Add
          </button>
        </div>
        <select
          className="w-full p-3 bg-black/30 rounded"
          onChange={(e) => setPaymentMethod(e.target.value)}
        >
          <option value="Cash">Cash</option>
          <option value="UPI">UPI</option>
          <option value="Card">Card</option>
        </select>
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            onChange={(e) => setIsRecurring(e.target.checked)}
          />
          <label>Recurring Expense</label>
        </div>
        {isRecurring && (
          <select
            className="w-full p-3 bg-black/30 rounded"
            onChange={(e) => setRecurringType(e.target.value)}
          >
            <option value="">Select Type</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        )}

        <button className="bg-green-600 px-4 py-2 rounded w-full">
          Save Expense
        </button>
      </form>
    </DashboardLayout>
  );
}

export default AddExpense;
