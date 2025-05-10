"use client";

import {useActivateUserMutation} from "@/lib/redux/slices/auth/authApiSlice";
import {useRouter} from "next/navigation";
import {useEffect} from "react";
import {toast} from "react-toastify";

interface AccountActivationProps {
  uid: string;
  token: string;
}


export default function AccountActivation({uid, token}: AccountActivationProps) {
  const [activateUser, {
    isLoading,
    isSuccess,
    isError
  }] = useActivateUserMutation();
  const router = useRouter();
  
  useEffect(() => {
    const activate = async () => {
      try {
        await toast.promise(
          activateUser({uid, token}).unwrap(),
          {
            pending: "Активуємо ваш акаунт...",
            success: "Акаунт було успішно активовано!",
          }
        );
        router.push("/login");
      } catch (error) {
        toast.error("Ваш акаунт уже активовано або посилання недійсне");
        router.push("/register");
      }
    };
    
    activate();
  }, [activateUser, uid, token, router]);
  
  return (
    <div className="w-full">
      {isLoading ? (
        <div className="flex items-center">
          <h2 className="text-xl">
            Триває активація вашого акаунту...
          </h2>
        </div>
      ) : isSuccess ? (
        <div className="flex items-center">
          <h2 className="text-xl">
            Ваш акаунт було успішно активовано!
          </h2>
        </div>
      ) : (
        isError && (
          <div className="flex items-center">
            <h2 className="text-xl">
              Ваш акаунт вже було активовано
            </h2>
          </div>
        )
      )}
    </div>
  );
}