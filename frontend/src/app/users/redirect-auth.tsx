"use client"
import { useAuthCtx } from "@/entity/users/context/auth";
import { redirect } from "next/navigation";
import { PropsWithChildren } from "react";

export function RedirectAuthenticated({ children }: PropsWithChildren) {
  const { isAuthenticated } = useAuthCtx()
  if (isAuthenticated) return redirect("/")
  return children;
}
