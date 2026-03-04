import { useState } from "react";
import AuthLayout from "../layouts/AuthLayout";
import { AccountAPI } from "../Api/axios";

function ForgotPassword() {
  const [email, setEmail] = useState("");

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await AccountAPI.post("sendresetpasswordemail/", { email });
      alert("Reset email sent successfully 📩");
    } catch (error: any) {
      alert(error.response?.data?.email || "Error sending email");
    }
  };

  return (
    <AuthLayout>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">
        Forgot Password
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Enter your email"
          className={inputStyle}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 
                     transition duration-300 p-3 rounded-xl 
                     text-white font-semibold"
        >
          Send Reset Link
        </button>
      </form>
    </AuthLayout>
  );
}

export default ForgotPassword;