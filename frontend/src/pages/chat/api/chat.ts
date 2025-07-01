"use client"

import { chatsService } from "@/entity/chats/api/chats"
import { IChatExtended } from "@/entity/chats/types"
import { useEffect, useState } from "react"

export function useChat(chatId: number) {
  const [chat, setChat] = useState<IChatExtended | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  useEffect(() => {
    const f = async () => {
      try {
        setIsLoading(true)
        const chat = await chatsService.getChat(chatId)
        setChat(chat)
        window.scroll({ behavior: "smooth", top: document.body.scrollHeight })
      } finally {
        setIsLoading(false)
      }
    }
    f()
  }, [chatId])
  return { isLoading, chat, setChat }
}
