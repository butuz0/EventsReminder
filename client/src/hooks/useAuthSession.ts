import {useAppDispatch, useAppSelector} from "@/lib/redux/hooks/reduxHooks";
import {useLogoutUserMutation} from "@/lib/redux/slices/auth/authApiSlice";
import {setLogout} from "@/lib/redux/slices/auth/authSlice";
import {useRouter} from "next/navigation";
import {toast} from "react-toastify";


export function useAuthSession() {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const [logoutUser] = useLogoutUserMutation();
  const {isAuthenticated} = useAppSelector((state) => state.auth);
  
  const logout = async () => {
    try {
      await logoutUser().unwrap();
      dispatch(setLogout());
      toast.success("Ви вийшли з акаунту");
      router.push("/login");
    } catch (e) {
      toast.error("Помилка під час виходу з акаунту");
    }
  };
  
  return {isAuthenticated, logout};
}
