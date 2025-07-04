import { DELETE, POST } from "@/shared/api/client"
import { ITelegramConnectConfirmPayload, ITelegramConnectInfo, ITelegramConnectRequestPayload } from "./types"
import { ITelegramAccountWithInfo } from "@/entity/users/types"
import { useEffect, useState } from "react"

export const requestTgConnect = async (data: ITelegramConnectRequestPayload) => {
  const resp = await POST<ITelegramConnectInfo>("/tg/connect/request", data)
  if (!resp.ok) {
    throw new Error(resp.detail)
  }
  return resp.data
}

export const confirmTgConnect = async (data: ITelegramConnectConfirmPayload) => {
  const resp = await POST<ITelegramAccountWithInfo>("/tg/connect/confirm", data)
  if (!resp.ok) {
    throw new Error(resp.detail)
  }
  return resp.data
}

export const tgDisconnect = async () => {
  const resp = await DELETE("/tg/logout")
  if (!resp.ok) {
    throw new Error(resp.detail)
  }
}
