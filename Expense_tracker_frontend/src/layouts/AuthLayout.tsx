import { motion } from "framer-motion";
import { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

function AuthLayout({ children }: Props) {
  return (
    <div className="min-h-screen bg-[#0F1115] flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="bg-white/5 backdrop-blur-xl border border-white/10 
                   rounded-3xl p-10 w-[420px] shadow-2xl"
      >
        {children}
      </motion.div>
    </div>
  );
}

export default AuthLayout;
