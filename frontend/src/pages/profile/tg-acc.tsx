import { ITelegramAccountWithInfo } from "@/entity/users/types";
import { UIButton } from "@/shared/ui/button";
import { tgDisconnect } from "./api/telegram";
import { useState } from "react";
import { Loader } from "@/shared/ui/loader";
import { useUserCtx } from "@/entity/users/context/user";

export function TgAccount({ acc }: { acc: ITelegramAccountWithInfo }) {
  const { setUser, user } = useUserCtx()
  const [isLoading, setIsLoading] = useState(false)
  if (isLoading) return <Loader />
  const handleDisconnect = async () => {
    try {
      setIsLoading(true)
      await tgDisconnect()
      setUser({ ...user!, tg: undefined })
    } finally {
      setIsLoading(false)
    }
  }
  return (
    <div>
      <h2 className="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Connected Telegram Account</h2>
      <div className="p-4 grid grid-cols-[20%_1fr] gap-x-6">
        <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#dbe1e6] py-5">
          <p className="text-[#60768a] text-sm font-normal leading-normal">ID</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.id}</p>
        </div>
        <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#dbe1e6] py-5">
          <p className="text-[#60768a] text-sm font-normal leading-normal">API ID</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.api_id}</p>
        </div>
        <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#dbe1e6] py-5">
          <p className="text-[#60768a] text-sm font-normal leading-normal">Phone Number</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.phone_number}</p>
        </div>
        <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#dbe1e6] py-5">
          <p className="text-[#60768a] text-sm font-normal leading-normal">Telegram username</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.info.username}</p>
        </div>
        <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#dbe1e6] py-5">
          <p className="text-[#60768a] text-sm font-normal leading-normal">Created At</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.created_at}</p>
        </div>
      </div>
      <UIButton onClick={handleDisconnect}>Disconnect</UIButton>
    </div>
  )
}
