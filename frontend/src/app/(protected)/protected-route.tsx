"use client"
import { useAuthCtx } from "@/entity/users/context/auth";
import { Loader } from "@/shared/ui/loader";
import { redirect } from "next/navigation";
import { PropsWithChildren } from "react";

export function ProtectedRoute({ children }: PropsWithChildren) {
  const { isAuthenticated, isLoading } = useAuthCtx()
  if (isLoading) return <Loader />
  if (!isAuthenticated) return redirect("/users/signin")
  return children;
}
