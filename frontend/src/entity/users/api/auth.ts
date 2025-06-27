import { GET, POST } from "@/shared/api/client"
import { ILoginForm, IRegisterForm, IUser } from "../types"

export const authService = {
  checkAuthenticated: async () => {
    const resp = await GET<{ is_authenticated: boolean }>("/auth/is-authenticated")
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data.is_authenticated
  },
  login: async (data: ILoginForm) => {
    const resp = await POST<IUser>("/auth/signin", data)
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  },
  register: async (data: IRegisterForm) => {
    const resp = await POST<IUser>("/auth/signup", data)
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  },
  logout: async () => {
    const resp = await POST("/auth/logout", {})
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
  }
}
