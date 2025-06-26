import { DEFAULT_AVATAR_URL } from "@/shared/constants/base";
import Image from "next/image";

export function Avatar({ className, size, src }: { className?: string, size: number, src?: string }) {
  return (
    <Image alt="user avatar" src={src || DEFAULT_AVATAR_URL} className={`rounded-full ${className || ''}`} width={size} height={size} />
  )
}
