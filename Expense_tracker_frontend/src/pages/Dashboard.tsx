import DashboardLayout from "../layouts/DashboardLayout";
import WalletCard from "./WalletCard";

function Dashboard() {
  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-6">
        Welcome to Dashboard 🚀
      </h1>
      <WalletCard />
    </DashboardLayout>
  );
}

export default Dashboard;