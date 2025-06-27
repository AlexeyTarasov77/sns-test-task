import { chatsService } from "@/entity/chats/api/chats"
import { IChat } from "@/entity/chats/types"
import { useEffect, useState } from "react"

export function useListChats(tgConnected: boolean) {
  const [chats, setChats] = useState<IChat[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(false)
  useEffect(() => {
    const f = async () => {
      try {
        setIsLoading(true)
        const chats = await chatsService.listTgChats()
        setChats(chats)
      } finally {
        setIsLoading(false)
      }
    }
    tgConnected && f()
  }, [tgConnected])
  return { isLoading, chats }
}
