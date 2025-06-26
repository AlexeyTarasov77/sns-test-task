import { ILoginForm, IRegisterForm } from "../types"

export const authService = {
  checkAuthenticated: async () => {
    return true
  },
  login: async (data: ILoginForm) => { },
  register: async (data: IRegisterForm) => { },
  logout: async () => { }
}
