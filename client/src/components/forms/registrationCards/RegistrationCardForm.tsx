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
} from "@/lib/validationSchemas/RegistrationCardValidationSchema";
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
import extractErrorMessage from "@/utils/extractErrorMessage";
import {useEffect} from "react";
import {addYears, format, isValid, parseISO} from "date-fns";

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
      organization_name: "Національний технічний університет України «КПІ імені Ігоря Сікорського»",
      edrpou_code: "02070921",
      region: "м. Київ",
      city: "Київ",
      full_name: undefined,
      id_number: undefined,
      keyword_phrase: undefined,
      voice_phrase: undefined,
      email: undefined,
      phone_number: undefined,
      electronic_seal_name: undefined,
      electronic_seal_keyword_phrase: undefined,
      issue_date: undefined,
      expiration_date: undefined
    }
  });
  
  // set the expiration_date to 2 years after issue_date
  useEffect(() => {
    const subscription = form.watch((value, {name}) => {
      if (name !== "issue_date") return;
      
      const issueDateRaw = value.issue_date;
      const issueDate = typeof issueDateRaw === "string"
        ? parseISO(issueDateRaw)
        : issueDateRaw;
      
      if (!isValid(issueDate)) return;
      
      const expirationDate = addYears(issueDate!, 2);
      form.setValue("expiration_date", format(expirationDate, "yyyy-MM-dd"), {
        shouldDirty: true,
        shouldTouch: true,
      });
    });
    
    return () => subscription.unsubscribe();
  }, [form]);
  
  const onSubmit = async (values: TRegistrationCardSchema) => {
    try {
      if (cardId) {
        await updateCard({card_id: cardId, data: values}).unwrap();
        toast.success("Картку оновлено успішно");
        router.push(`/documents/registration-cards/${cardId}/`);
      } else {
        const response = await createCard(values).unwrap();
        toast.success("Картку створено успішно");
        router.push(`/documents/registration-cards/${response?.registration_cards?.id}/`);
      }
      form.reset();
    } catch (error) {
      toast.error(`Під час додавання реєстраційної картки сталась помилка: ${extractErrorMessage(error)}`);
    }
  };
  
  return (
    <FormBase
      form={form}
      onSubmit={onSubmit}
    >
      <Accordion
        type="multiple"
        defaultValue={["item-3", "item-6"]}
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
        
        <AccordionItem
          value="item-6"
          className="border-b border-gray-300"
        >
          <AccordionTrigger className="text-lg hover:cursor-pointer">
            Дати
          </AccordionTrigger>
          <AccordionContent className="grid sm:grid-cols-2 gap-4">
            <FormField
              form={form}
              name="issue_date"
              label="Дата підписання"
              type="date"
            />
            <FormField
              form={form}
              name="expiration_date"
              label="Дата закінчення дії"
              type="date"
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
