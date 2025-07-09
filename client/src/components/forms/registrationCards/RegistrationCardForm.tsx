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
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

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
      <Accordion
        type="multiple"
        defaultValue={["item-1"]}
        className="space-y-5"
      >
        <AccordionItem
          value="item-1"
          className="border-b border-gray-300"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Юридична особа
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
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
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem
          value="item-2"
          className="border-b border-gray-300"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Відомості про місцезнаходження
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
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
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem
          value="item-3"
          className="border-b border-gray-300"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Дані заявника
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
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
              name="keyword_phrase"
              label="Ключова фраза"
            />
            <FormField
              form={form}
              name="voice_phrase"
              label="Голосова фраза"
            />
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem
          value="item-4"
          className="border-b border-gray-300"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Засоби звʼязку
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
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
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem
          value="item-5"
          className="border-b border-gray-300 last:border-none"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Кваліфікований сертифікат електронної печатки
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
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
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <div className="flex justify-center">
        <Button
          type="submit"
          disabled={isCreating || isUpdating}
          className="hover:cursor-pointer"
        >
          {cardId ? "Оновити картку" : "Додати картку"}
        </Button>
      </div>
    </FormBase>
  );
}
