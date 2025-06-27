import { GET } from "@/shared/api/client"
import { IChat } from "../types"

export const chatsService = {
  listTgChats: async () => {
    const resp = await GET<IChat[]>("/tg/chats")
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  },
}
