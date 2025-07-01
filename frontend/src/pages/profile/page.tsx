"use client"
import { useUserCtx } from "@/entity/users/context/user";
import { Loader } from "@/shared/ui/loader";
import { TgAccount } from "./tg-acc";
import { TgConnectForm } from "./tg-connect-form";

export function ProfilePage() {
  const { user, isLoading } = useUserCtx()
  if (isLoading) return <Loader />
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="flex flex-wrap justify-between gap-3 p-4"><p className="text-[#121416] tracking-light text-[32px] font-bold leading-tight min-w-72">Profile</p></div>
        {user &&
          <div>
            <p className="text-[#121416] text-base font-normal leading-normal pb-3 pt-1 px-4">Username: {user.username}</p>
            <p className="text-[#121416] text-base font-normal leading-normal pb-3 pt-1 px-4">Phone Number: {user.phone_number}</p>
          </div>
        }
        {user?.tg ? <TgAccount acc={user.tg} /> : <TgConnectForm />}
      </div>
    </div>
  )
}
