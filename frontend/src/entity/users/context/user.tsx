import { createContext, PropsWithChildren, useContext, useEffect, useState } from "react";
import {
  IUserExtended,
} from "../types";
import { usersService } from "../api/users";

interface IUserCtx {
  user: IUserExtended | null;
  isLoading: boolean;
}

export const UserCtx = createContext<IUserCtx | null>(null);

export function useUserCtx(): IUserCtx {
  const ctx = useContext(UserCtx);
  if (!ctx) throw new Error("ctx not provided");
  return ctx;
}

export function UsersProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<IUserExtended | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setIsLoading(true);
        const user = await usersService.getMe();
        setUser(user);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();
  }, []);


  return (
    <UserCtx.Provider
      value={{
        user,
        isLoading,
      }}
    >
      {children}
    </UserCtx.Provider>
  );
}

