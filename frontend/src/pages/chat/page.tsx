"use client"

import { Loader } from "@/shared/ui/loader"
import { useChat } from "./api/chat"
import { Message } from "./ui/message"
import { useEffect } from "react"
import { SERVER_URL } from "@/shared/constants"
import { IChatMessage } from "@/entity/chats/types"
import { toast } from "react-toastify"

export function ChatPage({ chatId }: { chatId: number }) {
  const { chat, setChat, isLoading } = useChat(chatId)
  const processNewMessages = (e: MessageEvent) => {
    setTimeout(() => {
      const messagesChunk: IChatMessage[] = JSON.parse(e.data).reverse()
      if (messagesChunk.length == 0) {
        toast("All messages have been loaded")
      }
      setChat(prev => (prev && { ...prev, messages: [...messagesChunk, ...prev.messages] }))
    }, 1000)
  }
  useEffect(() => {
    if (!chat) return
    const eventName = `chat_${chat.id}_messages`
    const es = new EventSource(SERVER_URL + "/events", { withCredentials: true });
    es.onopen = () => console.log(">>> Connection opened!");
    es.onerror = (e) => console.log("EventSource connection error!", e);
    es.addEventListener(eventName, processNewMessages)
    return () => {
      es.removeEventListener(eventName, processNewMessages)
      es.close()
    };
  }, [chatId, isLoading])
  if (isLoading) return <Loader />
  if (!chat) return
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <h1 className="text-[#111418] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 text-left pb-3 pt-5">{chat.title}</h1>
        {chat.messages.map(msg => <Message key={msg.id} msg={msg} />)}
      </div>
    </div>
  )
}
