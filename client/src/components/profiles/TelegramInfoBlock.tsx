import {Badge} from "@/components/ui/badge";
import InfoBlock from "@/components/shared/InfoBlock";

interface TelegramInfoBlockProps {
  username?: string,
  phoneNumber?: string,
  isVerified?: boolean
}


export default function TelegramInfoBlock({username, phoneNumber, isVerified = false}: TelegramInfoBlockProps) {
  return (
    <InfoBlock label="Telegram">
      <div className="grid grid-cols-3 gap-4 mt-2">
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
            Номер телефону
          </div>
          <div>
            {phoneNumber || "Не вказано"}
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