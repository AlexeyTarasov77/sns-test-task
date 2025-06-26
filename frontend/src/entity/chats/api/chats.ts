import { GET, POST } from "@/shared/api/client"
import { IChat, ITelegramConnectInfo } from "../types"

export const chatsService = {
  listTgChats: async () => {
    const resp = await GET<IChat>("/telegram/chats")
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  },
}
