"use client"
import { useAuthCtx } from "@/entity/users/context/auth";
import { IRegisterForm } from "@/entity/users/types";
import { UIButton } from "@/shared/ui/button";
import { UIInput } from "@/shared/ui/forms";
import { Loader } from "@/shared/ui/loader";
import { renderError } from "@/shared/utils/errors";
import { validationHelpers } from "@/shared/utils/validation";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";

export function SignUpPage() {
  const { control, register, setError, handleSubmit, formState: { errors } } = useForm<IRegisterForm>()
  const { signUp, isLoading } = useAuthCtx()
  const router = useRouter()
  const onSubmit = async (data: IRegisterForm) => {
    const errMsg = await signUp(data)
    if (errMsg) {
      return setError("root", { message: errMsg })
    }
    router.replace("/users/signin")
  }
  if (isLoading) return <Loader />
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="flex flex-col items-center py-5 max-w-[960px] flex-1 gap-4">
        <h2 className="text-[#111418] tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">Sign Up</h2>
        <div className="min-w-1/2">
          <UIInput.Text rules={validationHelpers.required()} label="Username" control={control} {...register("username")} />
        </div>
        <div className="min-w-1/2">
          <UIInput.Text rules={validationHelpers.required()} label="Phone number" type="tel" control={control} {...register("phone_number")} />
        </div>
        <div className="min-w-1/2">
          <UIInput.Text rules={{ ...validationHelpers.required(), ...validationHelpers.minLength(8) }} label="Password" type="password" control={control} {...register("password")} />
        </div>
        {renderError(errors.root)}
        <UIButton className="min-w-1/4" onClick={handleSubmit(onSubmit)}>Sign Up</UIButton>

        <Link href="/users/signin" className="text-[#60758a] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center underline">Already have an account? Sign In</Link>
      </div>
    </div>

  )
}
