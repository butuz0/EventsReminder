"use client";

import {setLogin, setLogout} from "@/lib/redux/slices/auth/authSlice";
import {useAppDispatch} from "@/lib/redux/hooks/reduxHooks";
import {getCookie} from "cookies-next";
import {useRouter} from "next/navigation";
import React, {useEffect, useState} from "react";
import LoaderComponent from "@/components/shared/Loader";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";


export default function ProtectedRoute({children}: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const [authChecked, setAuthChecked] = useState(false);
  
  const {
    data: user,
    isLoading: userLoading,
  } = useGetCurrentUserQuery();
  
  useEffect(() => {
    const checkAuth = async () => {
      const isLoggedIn = getCookie("logged_in") === "true";
      
      if (!isLoggedIn) {
        dispatch(setLogout());
        router.push("/login");
        return;
      }
      
      dispatch(setLogin());
      setAuthChecked(true);
    };
    
    checkAuth();
  }, [dispatch, router]);
  
  useEffect(() => {
    if (
      authChecked &&
      !userLoading &&
      user &&
      (!user.position || !user.department)
    ) {
      router.push("/register/profile");
    }
  }, [authChecked, userLoading, user, router]);
  
  if (!authChecked || userLoading) {
    return (
      <LoaderComponent size="xl" className="h-1/2"/>
    );
  }
  
  return <>{children}</>;
}