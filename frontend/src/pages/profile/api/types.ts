
export interface ITelegramConnectRequestPayload {
  api_id: number
  api_hash: string
  phone_number?: string;
}


export interface ITelegramConnectInfo {
  phone_number: string;
  phone_code_hash: string;
}

export interface ITelegramConnectConfirmPayload extends ITelegramConnectRequestPayload {
  phone_number: string;
  phone_code_hash: string;
  phone_code: string
  password?: string;
}
