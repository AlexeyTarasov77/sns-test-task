import { UIButton } from "@/shared/ui/button";
import { UIInput } from "@/shared/ui/forms";
import { useForm } from "react-hook-form";

export function TgConnectForm() {
  const { handleSubmit, register, control } = useForm()
  const onSubmit = async () => { }
  return (
    <div className="flex flex-col">
      <h2 className="text-[#121416] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Connect Telegram</h2>
      <p className="text-[#121416] text-base font-normal leading-normal pb-3 pt-1 px-4">Connect your Telegram account to manage your chats.</p>
      <div className="gap-4 flex flex-col">
        <UIInput.Text control={control} className="max-w-1/2" name="api_id" label="Enter your API ID" />
        <UIInput.Text control={control} className="max-w-1/2" name="api_hash" label="Enter your API HASH" />
        <UIInput.Text control={control} className="max-w-1/2" name="phone_number" label="Enter your phone number" />
      </div>
      <div className="flex justify-start mt-4">
        <UIButton className="max-w-1/4" onClick={handleSubmit(onSubmit)}>Connect Telegram</UIButton>
      </div>

    </div>
  )
}
