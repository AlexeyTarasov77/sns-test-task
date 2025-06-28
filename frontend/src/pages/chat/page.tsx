"use client"

import { Loader } from "@/shared/ui/loader"
import { useChat } from "./api/chat"
import { Message } from "./ui/message"

export function ChatPage({ chatId }: { chatId: number }) {
  const { chat, isLoading } = useChat(chatId)
  if (isLoading) return <Loader />
  if (!chat) return
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <h1 className="text-[#111418] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 text-left pb-3 pt-5">{chat.title}</h1>
        {chat.messages.map(msg => <Message msg={msg} />)}
      </div>
    </div>
  )
}
