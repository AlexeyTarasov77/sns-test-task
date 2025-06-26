"use client"
import { ILoginForm } from "@/entity/users/types";
import { UIButton } from "@/shared/ui/button";
import { UIInput } from "@/shared/ui/forms";
import Link from "next/link";
import { useForm } from "react-hook-form";

export function SignInPage() {
  const { control, register } = useForm<ILoginForm>()
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="flex flex-col items-center py-5 max-w-[960px] flex-1 gap-4">
        <h2 className="text-[#111418] tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">Welcome to Social Network Services</h2>
        <div className="min-w-1/2">
          <UIInput.Text label="Username" control={control} {...register("username")} />
        </div>
        <div className="min-w-1/2">
          <UIInput.Text label="Password" type="password" control={control} {...register("password")} />
        </div>

        <UIButton className="min-w-1/4">Login</UIButton>

        <Link href="/users/signup" className="text-[#60758a] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center underline">Don't have an account? Register</Link>
      </div>
    </div>

  )
}
