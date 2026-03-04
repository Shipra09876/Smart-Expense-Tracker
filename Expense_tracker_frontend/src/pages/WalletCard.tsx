import { useEffect, useState } from "react";
import { ExpenseAPI } from "../Api/axios";

function WalletCard() {
  const [wallet, setWallet] = useState<any>({});

  const fetchWallet = async () => {
    const res = await ExpenseAPI.get("get_wallet/");
    setWallet(res.data);
  };

  useEffect(() => {
    fetchWallet();
  }, []);

  return (
    <div className="bg-white/10 p-5 rounded-xl mb-6">
      <h2 className="text-xl mb-4">Wallet Balance</h2>
      <p>Main Wallet: ₹{wallet["Main Wallet"]}</p>
      <p>Saving Wallet: ₹{wallet["Saving Wallet"]}</p>
    </div>
  );
}

export default WalletCard;