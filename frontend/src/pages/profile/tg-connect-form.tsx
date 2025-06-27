import { UIButton } from "@/shared/ui/button";
import { UIInput } from "@/shared/ui/forms";
import { useForm } from "react-hook-form";
import { ITelegramConnectConfirmPayload, ITelegramConnectRequestPayload } from "./api/types";
import { confirmTgConnect, requestTgConnect } from "./api/telegram";
import { getErrorMessage, renderError } from "@/shared/utils/errors";
import { validationHelpers } from "@/shared/utils/validation";
import { useUserCtx } from "@/entity/users/context/user";

type ConnectFormDataT = ITelegramConnectRequestPayload & {
  phone_code_hash?: string;
  phone_code?: string
  password?: string;
}

export function TgConnectForm() {
  const { setUser, user } = useUserCtx()
  const { handleSubmit, control, setError, setValue, watch, formState: { errors } } = useForm<ConnectFormDataT>()
  const connectReqSent = !!watch("phone_code_hash")
  const onSubmit = async (data: ConnectFormDataT) => {
    if (connectReqSent) {
      try {
        const connected_tg = await confirmTgConnect(data as ITelegramConnectConfirmPayload)
        setUser({ ...user!, tg: connected_tg })
      }
      catch (err) {
        setError("root", { message: getErrorMessage(err) })
      }
      return
    }
    try {
      const { phone_number, phone_code_hash } = await requestTgConnect(data)
      setValue("phone_number", phone_number)
      setValue("phone_code_hash", phone_code_hash)
    } catch (err) {
      setError("root", { message: getErrorMessage(err) })
    }
  }
  return (
    <div className="flex flex-col">
      <h2 className="text-[#121416] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Connect Telegram</h2>
      <p className="text-[#121416] text-base font-normal leading-normal pb-3 pt-1 px-4">Connect your Telegram account to manage your chats.</p>
      <div className="gap-4 flex flex-col">
        <UIInput.Text rules={validationHelpers.required()} control={control} className="max-w-1/2" name="api_id" label="Enter your API ID" />
        <UIInput.Text rules={validationHelpers.required()} control={control} className="max-w-1/2" name="api_hash" label="Enter your API HASH" />
        <UIInput.Text rules={validationHelpers.required()} control={control} className="max-w-1/2" name="phone_number" label="Enter your phone number" />
        {connectReqSent && (
          <>
            <UIInput.Text rules={validationHelpers.required()} control={control} className="max-w-1/2" name="phone_code" label="Enter received phone code" />
            <UIInput.Text control={control} className="max-w-1/2" name="password" label="Enter 2fa password (if it's enabled on your account)" />
          </>
        )}
      </div>
      {renderError(errors.root)}
      <div className="flex justify-start mt-4">
        <UIButton className="max-w-1/4" onClick={handleSubmit(onSubmit)}>Connect Telegram</UIButton>
      </div>
    </div>
  )
}
