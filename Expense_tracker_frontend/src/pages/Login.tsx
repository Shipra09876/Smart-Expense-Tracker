import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import { AccountAPI } from "../Api/axios";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await AccountAPI.post("login/", form);

      // 🔥 Save tokens properly
      localStorage.setItem("access", res.data.token.access);
      localStorage.setItem("refresh", res.data.token.refresh);

      alert("Login successful 🚀");

      navigate("/dashboard");
    } catch (error: any) {
      console.log(error.response?.data);
      alert(error.response?.data?.error || "Invalid credentials");
    }
  };

  return (
    <AuthLayout>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">Login</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          className={inputStyle}
          required
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          className={inputStyle}
          required
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button
          type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 
                     transition duration-300 p-3 rounded-xl 
                     text-white font-semibold"
        >
          Login
        </button>
      </form>
      <p className="text-gray-400 text-sm mt-3 text-center">
        <Link to="/forgot-password" className="text-purple-400 hover:underline">
          Forgot Password?
        </Link>
      </p>

      <p className="text-gray-400 text-sm mt-2 text-center">
        <Link to="/otp-login" className="text-green-400 hover:underline">
          Login with OTP
        </Link>
      </p>

      <p className="text-gray-400 text-sm mt-4 text-center">
        Don’t have an account?{" "}
        <Link to="/signup" className="text-purple-400 hover:underline">
          Register
        </Link>
      </p>
    </AuthLayout>
  );
}

export default Login;
