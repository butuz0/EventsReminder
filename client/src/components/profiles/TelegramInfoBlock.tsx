"use client";

import {Badge} from "@/components/ui/badge";
import InfoBlock from "@/components/shared/InfoBlock";
import {useEffect, useRef} from "react";
import {useTelegramAuthMutation} from "@/lib/redux/slices/users/usersApiSlice";
import {toast} from "react-toastify";
import {TelegramAuthData} from "@/types";

interface TelegramInfoBlockProps {
  username?: string,
  isVerified?: boolean
}


export default function TelegramInfoBlock({username, isVerified = false}: TelegramInfoBlockProps) {
  const widgetRef = useRef<HTMLDivElement>(null);
  const [telegramAuth] = useTelegramAuthMutation();
  
  useEffect(() => {
    if (widgetRef.current && widgetRef.current.childNodes.length === 0) {
      const script = document.createElement("script");
      script.src = "https://telegram.org/js/telegram-widget.js?22";
      script.async = true;
      script.setAttribute("data-telegram-login", "kpi_notify_bot");
      script.setAttribute("data-size", "large");
      script.setAttribute("data-onauth", "onTelegramAuth(user)");
      script.setAttribute("data-request-access", "write");
      
      widgetRef.current.appendChild(script);
    }
    
    (window as any).onTelegramAuth = async function (user: TelegramAuthData) {
      try {
        await telegramAuth(user).unwrap();
        toast.success("Telegram-бота успішно підключено");
      } catch (error) {
        toast.error("Помилка при підключенні Telegram-бота");
      }
    };
  }, []);
  
  return (
    <InfoBlock label="Telegram">
      <div className="grid grid-cols-3 gap-4 mt-2">
        <div ref={widgetRef} className="flex justify-center"></div>
        <div className="text-center">
          <div className="text-gray-700 text-sm">
            Ім'я користувача
          </div>
          <div>
            {username || "Не вказано"}
          </div>
        </div>
        <div className="text-center">
          <div className="text-gray-700 text-sm">
            Статус
          </div>
          <div>
            <Badge
              variant="secondary"
              className={
                isVerified
                  ? "border-green-600 bg-green-100 text-green-800"
                  : "border-red-600 bg-red-100 text-red-800"
              }
            >
              {isVerified ? "Підтверджено" : "Не підтверджено"}
            </Badge>
          </div>
        </div>
      </div>
    </InfoBlock>
  )
}