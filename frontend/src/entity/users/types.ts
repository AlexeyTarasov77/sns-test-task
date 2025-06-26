
export interface ILoginForm {
  username: string;
  password: string;
}
export interface IRegisterForm extends ILoginForm {
  phone_number: string;
}

export interface IUser extends IRegisterForm {
  id: number;
  avatar_url?: string;
}

export interface ITelegramAccountInfo {
  first_name?: string
  last_name?: string
  username: string
  photo_url?: string
}

export interface ITelegramAccount {
  id: number
  api_id: number
  phone_number: string
  created_at: string
  info: ITelegramAccountInfo
}

export interface IUserExtended extends IUser {
  tg: ITelegramAccount
}
