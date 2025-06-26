import { useAuthCtx } from "@/entity/users/context/auth";
import { redirect } from "next/navigation";
import { PropsWithChildren } from "react";

export default function Layout({
  children,
}: PropsWithChildren) {
  const { isAuthenticated } = useAuthCtx()
  if (!isAuthenticated) return redirect("/users/signin")
  return children;
}
