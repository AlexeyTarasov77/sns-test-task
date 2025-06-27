"use client"
import { useAuthCtx } from "@/entity/users/context/auth";
import { Loader } from "@/shared/ui/loader";
import { redirect } from "next/navigation";
import { PropsWithChildren } from "react";

export function RedirectAuthenticated({ children }: PropsWithChildren) {
  const { isAuthenticated, isLoading } = useAuthCtx()
  if (isLoading) return <Loader />
  if (isAuthenticated) return redirect("/")
  return children;
}
