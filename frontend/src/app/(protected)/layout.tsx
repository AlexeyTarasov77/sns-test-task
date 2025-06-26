import { PropsWithChildren } from "react";
import { ProtectedRoute } from "./protected-route";

export default function Layout({
  children,
}: PropsWithChildren) {
  return <ProtectedRoute>{children}</ProtectedRoute>;
}
