import {
  createContext,
  PropsWithChildren,
  useContext,
  useEffect,
  useState,
} from "react";
import {
  ILoginForm,
  IRegisterForm,
} from "../types";
import { authService } from "../api/auth";
import { getErrorMessage } from "@/shared/utils/errors";

interface IAuthCtx {
  isLoading: boolean;
  login: (data: ILoginForm) => Promise<string | void>;
  register: (data: IRegisterForm) => Promise<string | void>;
  logout: () => void;
  isAuthenticated: boolean
}

export const AuthCtx = createContext<IAuthCtx | null>(null);

export function useAuthCtx(): IAuthCtx {
  const ctx = useContext(AuthCtx);
  if (!ctx) throw new Error("ctx not provided");
  return ctx;
}


export function AuthProvider({ children }: PropsWithChildren) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const f = async () => {
      try {
        setIsLoading(true);
        const isAuthenticated = await authService.checkAuthenticated();
        setIsAuthenticated(isAuthenticated)
      } finally {
        setIsLoading(false);
      }
    };

    f();
  }, []);


  const login = async (data: ILoginForm) => {
    try {
      setIsLoading(true);
      await authService.login(data);
      setIsAuthenticated(true)
    } catch (err) {
      return getErrorMessage(err);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: IRegisterForm) => {
    try {
      setIsLoading(true);
      await authService.register(data);
    } catch (err) {
      return getErrorMessage(err);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      setIsLoading(true);
      await authService.logout();
      setIsAuthenticated(false)
    } catch (err) {
      return getErrorMessage(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthCtx.Provider
      value={{
        login,
        register,
        isLoading,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthCtx.Provider>
  );
}

