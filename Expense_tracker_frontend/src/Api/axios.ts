import axios from "axios";

const BASE_URL = "http://54.174.198.97:8001/api/";

/* ===============================
   ACCOUNT API (Login/Register)
================================= */
export const AccountAPI = axios.create({
  baseURL: BASE_URL + "account/",
});

/* ===============================
   EXPENSE API (Income/Wallet/etc)
================================= */
export const ExpenseAPI = axios.create({
  baseURL: BASE_URL + "expense/",
});

/* ===============================
   Attach Token Interceptor
================================= */

const attachToken = (req: any) => {
  const token = localStorage.getItem("access");

  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }

  return req;
};

ExpenseAPI.interceptors.request.use(attachToken);
AccountAPI.interceptors.request.use((req) => {
  const token = localStorage.getItem("access");

  const authRoutes = [
    "login/",
    "register/",
    "sendresetpasswordemail/",
    "resetpassword/",
    "login_otp/",
    "verify_otp/",
  ];

  const shouldSkip = authRoutes.some((route) =>
    req.url?.includes(route)
  );

  if (token && !shouldSkip) {
    req.headers.Authorization = `Bearer ${token}`;
  }

  return req;
});