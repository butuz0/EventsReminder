"use client";

import {useParams} from "next/navigation";
import {useGetRegistrationCardDetailsQuery} from "@/lib/redux/slices/registrationCards/registrationCardsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import RegistrationCardForm from "@/components/forms/registrationCards/RegistrationCardForm";
import FormHeader from "@/components/forms/FormHeader";


export default function EditRegistrationCardPage() {
  const {card_id} = useParams<{ card_id: string }>();
  const {data: card, isLoading, isError} = useGetRegistrationCardDetailsQuery(card_id);
  
  if (isLoading) {
    return <LoaderComponent size="xl" text="Завантаження картки для редагування..."/>;
  }
  
  if (isError || !card) {
    return <p className="text-red-600 text-center">Не вдалося завантажити дані картки</p>;
  }
  
  return (
    <div className="max-w-3xl mx-auto bg-white p-6 shadow-md rounded-xl">
      <FormHeader title="Редагування картки АЦСК"/>
      <RegistrationCardForm
        cardId={card_id}
        defaultValues={card}
      />
    </div>
  );
}
