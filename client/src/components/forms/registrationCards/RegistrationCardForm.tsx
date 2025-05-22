"use client";

import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "react-toastify";
import {Button} from "@/components/ui/button";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {
  RegistrationCardSchema,
  TRegistrationCardSchema
} from "@/lib/validationSchemas/registrationCardValidationSchema";
import {
  useCreateRegistrationCardMutation,
  useUpdateRegistrationCardMutation
} from "@/lib/redux/slices/registrationCards/registrationCardsApiSlice";
import {useRouter} from "next/navigation";

interface RegistrationCardFormProps {
  cardId?: string;
  defaultValues?: TRegistrationCardSchema;
}


export default function RegistrationCardForm(
  {
    cardId,
    defaultValues
  }: RegistrationCardFormProps) {
  const [createCard, {isLoading: isCreating}] = useCreateRegistrationCardMutation();
  const [updateCard, {isLoading: isUpdating}] = useUpdateRegistrationCardMutation();
  const router = useRouter();
  
  const form = useForm<TRegistrationCardSchema>({
    resolver: zodResolver(RegistrationCardSchema),
    mode: "all",
    defaultValues: defaultValues || {
      organization_name: "",
      edrpou_code: "",
      region: "",
      city: "",
      full_name: "",
      id_number: "",
      keyword_phrase: "",
      voice_phrase: "",
      email: "",
      phone_number: "",
      electronic_seal_name: "",
      electronic_seal_keyword_phrase: ""
    }
  });
  
  const onSubmit = async (values: TRegistrationCardSchema) => {
    try {
      if (cardId) {
        await updateCard({card_id: cardId, data: values}).unwrap();
        toast.success("Картку оновлено успішно");
      } else {
        await createCard(values).unwrap();
        toast.success("Картку створено успішно");
      }
      form.reset();
      router.push("/profile/");
    } catch {
      toast.error("Помилка під час збереження картки");
    }
  };
  
  return (
    <FormBase
      form={form}
      onSubmit={onSubmit}
    >
      <FormField
        form={form}
        name="organization_name"
        label="Назва організації"
      />
      <FormField
        form={form}
        name="edrpou_code"
        label="Код ЄДРПОУ"
      />
      <FormField
        form={form}
        name="region"
        label="Область"
      />
      <FormField
        form={form}
        name="city"
        label="Місто"
      />
      <FormField
        form={form}
        name="full_name"
        label="ПІБ"
      />
      <FormField
        form={form}
        name="id_number"
        label="Ідентифікаційний номер"
      />
      <FormField
        form={form}
        name="email"
        label="Email"
      />
      <FormField
        form={form}
        name="phone_number"
        label="Номер телефону"
      />
      <FormField
        form={form}
        name="keyword_phrase"
        label="Ключова фраза"
      />
      <FormField
        form={form}
        name="voice_phrase"
        label="Голосова фраза"
      />
      <FormField
        form={form}
        name="electronic_seal_name"
        label="Назва Е-печатки"
      />
      <FormField
        form={form}
        name="electronic_seal_keyword_phrase"
        label="Ключова фраза до печатки"
      />
      <div className="flex justify-center">
        <Button
          type="submit"
          disabled={isCreating || isUpdating}
        >
          {cardId ? "Оновити" : "Створити"}
        </Button>
      </div>
    </FormBase>
  );
}
