"use client";

import {useEffect} from "react";
import {getCookie} from "cookies-next";
import {useAppDispatch} from "@/lib/redux/hooks/reduxHooks";
import {setLogin, setLogout} from "@/lib/redux/slices/auth/authSlice";


export default function AuthInitializer() {
  const dispatch = useAppDispatch();
  
  useEffect(() => {
    if (getCookie("logged_in") === "true") {
      dispatch(setLogin());
    } else {
      dispatch(setLogout());
    }
  }, [dispatch]);
  
  return null;
}