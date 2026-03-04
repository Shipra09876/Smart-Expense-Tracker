import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import { AccountAPI } from "../Api/axios";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    username: "",
    name: "",
    phone_no: "",
    password: "",
    password2: "",
    tc: false,
    profile_picture: null,
    dob: "",
    occupation: "",
    monthly_income: 0,
    currency: "rs",
  });

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.tc) {
      alert("Please accept terms & conditions");
      return;
    }

    if (form.password !== form.password2) {
      alert("Passwords do not match");
      return;
    }

    try {
      const res = await AccountAPI.post("register/", form);

      // ✅ Store tokens
      localStorage.setItem("access", res.data.token.access);
      localStorage.setItem("refresh", res.data.token.refresh);

      alert("Account created successfully 🚀");
      navigate("/dashboard");

    } catch (err: any) {
      console.log(err.response?.data);
      alert("Registration failed");
    }
  };

  return (
    <AuthLayout>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">
        Create Account
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">

        <input type="text" placeholder="Username"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />

        <input type="text" placeholder="Full Name"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input type="text" placeholder="Phone Number"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, phone_no: e.target.value })}
        />

        <input type="email" placeholder="Email"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input type="date"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, dob: e.target.value })}
        />

        <input type="text" placeholder="Occupation"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, occupation: e.target.value })}
        />

        <input type="number" placeholder="Monthly Income"
          className={inputStyle}
          onChange={(e) =>
            setForm({ ...form, monthly_income: Number(e.target.value) })
          }
        />

        <input type="password" placeholder="Password"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <input type="password" placeholder="Confirm Password"
          className={inputStyle}
          onChange={(e) => setForm({ ...form, password2: e.target.value })}
        />

        <div className="flex items-center space-x-2">
          <input type="checkbox"
            onChange={(e) => setForm({ ...form, tc: e.target.checked })}
          />
          <label className="text-gray-300 text-sm">
            I agree to Terms & Conditions
          </label>
        </div>

        <button type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 
                     transition duration-300 p-3 rounded-xl 
                     text-white font-semibold"
        >
          Sign Up
        </button>
      </form>

      <p className="text-gray-400 text-sm mt-4 text-center">
        Already have an account?{" "}
        <Link to="/login" className="text-purple-400 hover:underline">
          Login
        </Link>
      </p>
    </AuthLayout>
  );
}

export default Register;