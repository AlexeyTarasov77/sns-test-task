
export interface ILoginForm {
  username: string;
  password: string;
}
export interface IRegisterForm extends ILoginForm {
  phone_number: string;
}

export interface IUser extends IRegisterForm {
  id: number;
}

export interface IUserTgAcc {

}

export interface IUserExtended extends IUser {
  tg: IUserTgAcc
}
