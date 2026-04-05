import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import ChangePassword from "./pages/ChangePassword";
import OtpLogin from "./pages/OtpLogin";
import ResetPassword from "./pages/ResetPassword";
import ForgotPassword from "./pages/ForgotPassword";
import Income from "./pages/Income";
import AddIncome from "./pages/AddIncome";
import WalletCard from "./pages/WalletCard";
import Expense from "./pages/Expense";
import EditIncome from "./pages/EditIncome";
import EditExpense from "./pages/EditExpense";
import AddExpense from "./pages/AddExpense";
import Recurring from "./pages/Recurring";
import AddRecurring from "./pages/AddRecurring";
import Goals from "./pages/Goals";
import AddGoal from "./pages/AddGoal";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset_password/:uid/:token" element={<ResetPassword />} />
        <Route
          path="/change-password"
          element={
            <ProtectedRoute>
              <ChangePassword />
            </ProtectedRoute>
          }
        />
        <Route
          path="/income"
          element={
            <ProtectedRoute>
              <Income />
            </ProtectedRoute>
          }
        />
        <Route
          path="/walletcard"
          element={
            <ProtectedRoute>
              <WalletCard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/expenses"
          element={
            <ProtectedRoute>
              <Expense />
            </ProtectedRoute>
          }
        />
        <Route path="/add-income" element={<AddIncome />} />
        <Route path="/otp-login" element={<OtpLogin />} />
        <Route path="/add-expense" element={<AddExpense />} />
        <Route
          path="/edit-expense/:id"
          element={
            <ProtectedRoute>
              <EditExpense />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recurring"
          element={
            <ProtectedRoute>
              <Recurring />
            </ProtectedRoute>
          }
        />

        <Route path="/add-recurring" element={<AddRecurring />} />

        <Route
          path="/goals"
          element={
            <ProtectedRoute>
              <Goals />
            </ProtectedRoute>
          }
        />

        <Route path="/add-goal" element={<AddGoal />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
