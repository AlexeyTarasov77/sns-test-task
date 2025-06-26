import { POST } from "@/shared/api/client"
import { ITelegramConnectConfirmPayload, ITelegramConnectInfo, ITelegramConnectRequestPayload } from "./types"
import { ITelegramAccount } from "@/entity/users/types"

export const requestTgConnect = async (data: ITelegramConnectRequestPayload) => {
  const resp = await POST<ITelegramConnectInfo>("/tg/connect/request", data)
  if (!resp.ok) {
    throw new Error(resp.detail)
  }
  return resp.data
}

export const confirmTgConnect = async (data: ITelegramConnectConfirmPayload) => {
  const resp = await POST<ITelegramAccount>("/tg/connect/confirm", data)
  if (!resp.ok) {
    throw new Error(resp.detail)
  }
  return resp.data
}

