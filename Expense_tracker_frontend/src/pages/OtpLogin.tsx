import { useState } from "react";
import AuthLayout from "../layouts/AuthLayout";
import { AccountAPI } from "../Api/axios";
import { useNavigate } from "react-router-dom";

function OtpLogin() {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await AccountAPI.post("login_otp/", { email, password });
      alert("OTP sent to your email 📩");
      setStep(2);
    } catch {
      alert("Invalid credentials");
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await AccountAPI.post("verify_otp/", { email, otp });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      navigate("/dashboard");
    } catch {
      alert("Invalid OTP");
    }
  };

  return (
    <AuthLayout>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">
        OTP Login
      </h2>

      {step === 1 ? (
        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className={inputStyle}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className={inputStyle}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="w-full bg-purple-600 p-3 rounded-xl">
            Send OTP
          </button>
        </form>
      ) : (
        <form onSubmit={handleVerify} className="space-y-4">
          <input
            type="text"
            placeholder="Enter OTP"
            className={inputStyle}
            onChange={(e) => setOtp(e.target.value)}
          />

          <button className="w-full bg-green-600 p-3 rounded-xl">
            Verify OTP
          </button>
        </form>
      )}
    </AuthLayout>
  );
}

export default OtpLogin;