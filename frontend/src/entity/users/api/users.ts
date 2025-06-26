import { GET } from "@/shared/api/client";
import { IUserExtended } from "../types";

export const usersService = {
  getMe: async (): Promise<IUserExtended> => {
    const resp = await GET<IUserExtended>("/auth/me")
    if (!resp.ok) {
      throw new Error(resp.detail)
    }
    return resp.data
  }
}
