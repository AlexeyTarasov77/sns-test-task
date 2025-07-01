"use client"
import { useAuthCtx } from "@/entity/users/context/auth";
import { Loader } from "@/shared/ui/loader";
import { redirect } from "next/navigation";
import { PropsWithChildren, useEffect, useState } from "react";

export function ProtectedRoute({ children }: PropsWithChildren) {
  const { isAuthenticated, isLoading } = useAuthCtx()
  const [shouldRedirect, setShouldRedirect] = useState<boolean | null>(null)
  console.log(isLoading, isAuthenticated)
  useEffect(() => {
    if (isLoading) return
    const timeout = setTimeout(() => isAuthenticated ? setShouldRedirect(false) : setShouldRedirect(true), 500)
    return () => clearTimeout(timeout)
  }, [isLoading, isAuthenticated])
  if (isLoading || shouldRedirect === null) return <Loader />
  return shouldRedirect ? redirect("/users/signin") : children;
}
