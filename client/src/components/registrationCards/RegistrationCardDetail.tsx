"use client";

import {
  useGetRegistrationCardDetailsQuery
} from "@/lib/redux/slices/registrationCards/registrationCardsApiSlice";
import InfoBlock from "@/components/shared/InfoBlock";
import LoaderComponent from "@/components/shared/Loader";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import RegistrationCardDeleteButton from "@/components/registrationCards/RegistrationCardDeleteButton";

interface RegistrationCardDetailProps {
  cardId: string;
}


export default function RegistrationCardDetail({cardId}: RegistrationCardDetailProps) {
  const {data: card, isLoading, isError} = useGetRegistrationCardDetailsQuery(cardId);
  
  if (isLoading) {
    return <LoaderComponent size="xl" text="Завантаження картки..."/>
  }
  
  if (isError || !card) {
    return <p className="text-center text-red-600 font-medium">Не вдалося завантажити картку</p>
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-6 bg-gray-100
    p-6 rounded-xl shadow-md text-sm border border-gray-200">
      <div className="space-y-2 bg-white p-4 rounded-md shadow-sm">
        <h2 className="text-lg font-semibold">
          Юридична особа
        </h2>
        <InfoBlock label="Назва організації">
          {card.organization_name}
        </InfoBlock>
        <InfoBlock label="Код ЄДРПОУ">
          {card.edrpou_code || "Не вказано"}
        </InfoBlock>
      </div>
      
      <div className="space-y-2 bg-white p-4 rounded-md shadow-sm">
        <h2 className="text-lg font-semibold">
          Відомості про місцезнаходження
        </h2>
        <InfoBlock label="Область">
          {card.region || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="Населений пункт">
          {card.city || "Не вказано"}
        </InfoBlock>
      </div>
      
      <div className="space-y-2 bg-white p-4 rounded-md shadow-sm">
        <h2 className="text-lg font-semibold">
          Дані заявника
        </h2>
        <InfoBlock label="ПІБ">
          {card.full_name || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="ІПН / ID номер">
          {card.id_number || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="Питання до ключової фрази">
          {card.keyword_phrase || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="Ключова фраза голосової аутентифікації">
          {card.voice_phrase || "Не вказано"}
        </InfoBlock>
      </div>
      
      <div className="space-y-2 bg-white p-4 rounded-md shadow-sm">
        <h2 className="text-lg font-semibold">
          Засоби звʼязку
        </h2>
        <InfoBlock label="Телефон">
          {card.phone_number || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="Електронна пошта">
          {card.email || "Не вказано"}
        </InfoBlock>
      </div>
      
      <div className="space-y-2 bg-white p-4 rounded-md shadow-sm">
        <h2 className="text-lg font-semibold">
          Кваліфікований сертифікат електронної печатки
        </h2>
        <InfoBlock label="Назва електронної печатки">
          {card.electronic_seal_name || "Не вказано"}
        </InfoBlock>
        <InfoBlock label="Ключова фраза до печатки">
          {card.electronic_seal_keyword_phrase || "Не вказано"}
        </InfoBlock>
      </div>
      
      <div className="flex justify-between">
        <RegistrationCardDeleteButton registrationCardId={card.id}/>
        
        <Button asChild>
          <Link href={`/profile/registration-cards/${cardId}/update/`}>
            Оновити картку
          </Link>
        </Button>
      </div>
    </div>
  );
}
