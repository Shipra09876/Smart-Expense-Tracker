import { useState } from "react";
import { useParams } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import { AccountAPI } from "../Api/axios";

function ResetPassword() {
  const { uid, token } = useParams();

  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await AccountAPI.post(`resetpassword/${uid}/${token}/`, {
        password,
        password2,
      });

      alert("Password reset successfully 🎉");
    } catch (error: any) {
      alert("Invalid or expired token");
    }
  };

  return (
    <AuthLayout>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">
        Reset Password
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="password"
          placeholder="New Password"
          className={inputStyle}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirm Password"
          className={inputStyle}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 
                     transition duration-300 p-3 rounded-xl 
                     text-white font-semibold"
        >
          Reset Password
        </button>
      </form>
    </AuthLayout>
  );
}

export default ResetPassword;