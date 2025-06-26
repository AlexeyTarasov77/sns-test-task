import { ILoginForm, IRegisterForm } from "../types"

export const authService = {
  checkAuthenticated: async () => {
    return false
  },
  login: async (data: ILoginForm) => { },
  register: async (data: IRegisterForm) => { },
  logout: async () => { }
}
