import { PropsWithChildren } from "react";
import { RedirectAuthenticated } from "./redirect-auth";

export default function Layout({
  children,
}: PropsWithChildren) {
  return <RedirectAuthenticated>{children}</RedirectAuthenticated>
}
