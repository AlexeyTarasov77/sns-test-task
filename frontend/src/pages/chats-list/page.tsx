"use client"
import { useUserCtx } from "@/entity/users/context/user"
import { Loader } from "@/shared/ui/loader"

export function ChatsListPage() {
  const { user, isLoading } = useUserCtx()
  if (isLoading) return <Loader />
  if (!user?.tg) {
    return <h1 className="text-center text-2xl mt-5">You don't have telegram account connected yet. Connect it to view chats list</h1>
  }
  return (
    <div>
      <h1>Chats list</h1>
    </div>
  )
}
