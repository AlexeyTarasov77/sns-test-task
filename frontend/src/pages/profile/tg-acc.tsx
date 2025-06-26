import { ITelegramAccountWithInfo } from "@/entity/users/types";

export function TgAccount({ acc }: { acc: ITelegramAccountWithInfo }) {
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
          <p className="text-[#60768a] text-sm font-normal leading-normal">Created At</p>
          <p className="text-[#111518] text-sm font-normal leading-normal">{acc.created_at}</p>
        </div>
      </div>
    </div>
  )
}
