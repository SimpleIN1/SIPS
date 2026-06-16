import { Navigate } from "react-router-dom";
import { useAppSelector } from "@/hooks/hook";

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const isAuth = useAppSelector((s) => s.user.isAuth);

  if (!isAuth) return <Navigate to="/authorization" replace />;
  return children;
}