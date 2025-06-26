import { ButtonHTMLAttributes, DetailedHTMLProps, ReactNode } from "react";

export function UIButton({ children, className, ...btnProps }: DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> & { children?: ReactNode }) {
  return (
    <button
      {...btnProps}
      className={`flex cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 py-3 flex-1 bg-[#0c7ff2] text-white text-sm font-bold leading-normal tracking-[0.015em] ${className || ''}`}
    >
      {children}
    </button>
  )
}
