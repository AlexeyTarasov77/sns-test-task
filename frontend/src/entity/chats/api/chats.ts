import { GET } from "@/shared/api/client"
import { IChat, IChatExtended } from "../types"

export const chatsService = {
  listTgChats: async () => {
    const resp = await GET<IChat[]>("/tg/chats")
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  },
  getChat: async (chatId: number) => {
    const resp = await GET<IChatExtended>("/tg/chats/" + String(chatId))
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    resp.data.messages.reverse()
    return resp.data
  }
}
