import { ITelegramAccountInfo } from "../users/types";

export interface IChat {
  id: number;
  title: string;
  photo_url?: string;
  last_message?: string
}

export interface IChatMessage {
  id: number
  date: string
  out: boolean
  message: string
  reply_to_msg_id?: number
  sender: ITelegramAccountInfo
}

export interface IChatExtended extends Omit<IChat, "last_message"> {
  messages: IChatMessage[]
}
