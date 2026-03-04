import { useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { AccountAPI } from "../Api/axios";

function ChangePassword() {
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await AccountAPI.post("changepassword/", {
        password,
        password2,
      });

      alert("Password changed successfully 🔒");
    } catch (error: any) {
      alert("Error changing password");
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-8">Change Password</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
        <input
          type="password"
          placeholder="New Password"
          className={inputStyle}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="Confirm Password"
          className={inputStyle}
          onChange={(e) => setPassword2(e.target.value)}
        />

        <button
          type="submit"
          className="bg-purple-600 px-4 py-2 rounded-lg"
        >
          Change Password
        </button>
      </form>
    </DashboardLayout>
  );
}

export default ChangePassword;