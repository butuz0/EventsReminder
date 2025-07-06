import {useAppSelector} from "@/lib/redux/hooks/reduxHooks";
import {useRouter} from "next/navigation";
import {useEffect} from "react";


export default function useRedirectIfAuthenticated() {
  const router = useRouter();
  const isAuthenticated = useAppSelector((state) =>
    state.auth.isAuthenticated
  );
  
  useEffect(() => {
    if (isAuthenticated) {
      router.push("/home");
    }
  }, [isAuthenticated, router]);
};