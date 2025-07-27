"use client";

import FormBase from "@/components/forms/FormBase";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {RecurrenceRuleOptions, PriorityOptions} from "@/constants";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "react-toastify";
import {useCreateEventMutation, useCreateRecurringEventMutation} from "@/lib/redux/slices/events/eventsApiSlice";
import {useCreateNotificationMutation} from "@/lib/redux/slices/notifications/notificationsApiSlice";
import {
  EventWithNotificationsSchema,
  TEventWithNotificationsSchema
} from "@/lib/validationSchemas/EventSchema";
import {
  MapPinIcon,
  CalendarIcon,
  PhotoIcon,
  LinkIcon,
  ClipboardDocumentListIcon,
  ArrowPathIcon,
  ExclamationCircleIcon
} from "@heroicons/react/24/outline";
import FormHeader from "@/components/forms/FormHeader";
import objToFormData from "@/utils/objToFormData";
import TagInputField from "@/components/forms/TagInputField";
import NotificationsFieldArray from "@/components/forms/events/NotificationsFieldArray";
import AssignToSelectField from "@/components/teams/AssignToSelectField";
import {RecurringEventSchema, TRecurringEventSchema} from "@/lib/validationSchemas/RecurringEventSchema";
import CheckboxField from "@/components/forms/CheckboxField";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import extractErrorMessage from "@/utils/extractErrorMessage";

interface EventFormProps {
  teamId?: string;
}


export default function EventCreateForm({teamId}: EventFormProps) {
  const router = useRouter();
  
  const [createEvent, {isLoading}] = useCreateEventMutation();
  const [createRecurringEvent] = useCreateRecurringEventMutation();
  const [createNotification] = useCreateNotificationMutation();
  
  const form = useForm<TEventWithNotificationsSchema>({
    resolver: zodResolver(EventWithNotificationsSchema),
    mode: "all",
    defaultValues: {
      title: "",
      description: undefined,
      start_datetime: undefined,
      location: undefined,
      link: undefined,
      priority: 2,
      image: undefined,
      tags: [],
      team: teamId ?? undefined,
      assigned_to_ids: [],
      is_recurring: false,
      notifications: []
    },
  });
  
  const recurringForm = useForm<TRecurringEventSchema>({
    resolver: zodResolver(RecurringEventSchema),
    mode: "all",
    defaultValues: {
      recurrence_rule: "w",
      recurrence_end_datetime: undefined,
    }
  })
  
  const isRecurring = form.watch("is_recurring");
  
  const onSubmit = async (values: TEventWithNotificationsSchema) => {
    try {
      const {notifications, ...eventValues} = values;
      
      // convert to FormData if an image was provided
      const hasImage = eventValues.image instanceof File;
      const data = hasImage
        ? objToFormData(eventValues)
        : eventValues;
      
      // create new event
      const response = await toast.promise(
        createEvent(data).unwrap(),
        {
          pending: "Додаємо подію...",
          success: "Подію додано",
        }
      );
      
      // create recurring event
      if (isRecurring) {
        const recurringValues = recurringForm.getValues();
        await createRecurringEvent({
          event_id: response.event.id,
          data: recurringValues
        }).unwrap();
      }
      
      // create notifications for a new event
      if (notifications.length > 0) {
        await Promise.all(
          notifications.map((n) =>
            createNotification({
              ...n,
              content_type: "event",
              object_id: response.event.id,
            }).unwrap()
          )
        );
      }
      
      router.push(`/events/${response.event.id}`);
      form.reset();
    } catch (error) {
      toast.error(`При додаванні події сталась помилка: ${extractErrorMessage(error)}`)
    }
  }
  
  return (
    <div className="w-full max-w-3xl bg-white p-5 rounded-xl
    border border-sky-200 shadow-md flex flex-col justify-center">
      <FormHeader
        title="Додайте нову подію"
      />
      <FormBase
        form={form}
        onSubmit={onSubmit}
        className="w-full"
        encType="multipart/form-data"
      >
        <FormField
          form={form}
          name="title"
          label="Назва події"
          placeholder="Назва нової події"
          icon={<ClipboardDocumentListIcon className="w-7"/>}
        />
        
        <FormField
          form={form}
          name="start_datetime"
          label="Дата та час"
          type="datetime-local"
          icon={<CalendarIcon className="w-7"/>}
        />
        
        <SelectFieldComponent
          form={form}
          name="priority"
          label="Пріоритет"
          options={PriorityOptions}
          placeholder="Оберіть пріоритет події"
          icon={<ExclamationCircleIcon className="w-7"/>}
        />
        
        <CheckboxField
          form={form}
          name="is_recurring"
          label="Повторювана подія"
        />
        
        {isRecurring && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <SelectFieldComponent
              form={recurringForm}
              name="recurrence_rule"
              label="Періодичність"
              options={RecurrenceRuleOptions}
              icon={<ArrowPathIcon className="w-7"/>}
            />
            <FormField
              form={recurringForm}
              name="recurrence_end_datetime"
              label="Завершення повторень"
              type="datetime-local"
              icon={<CalendarIcon className="w-7"/>}
            />
          </div>
        )}
        <Accordion
          type="multiple"
          className="mb-0"
        >
          <AccordionItem
            value="additional"
            className="border-t border-gray-300"
          >
            <AccordionTrigger className="text-lg">
              Додаткова інформація
            </AccordionTrigger>
            <AccordionContent className="space-y-5">
              <FormField
                form={form}
                name="description"
                label="Опис"
                placeholder="Опис події"
                isTextarea
              />
              <TagInputField
                form={form}
                name="tags"
                label="Теги"
              />
              <FormField
                form={form}
                name="location"
                label="Місце"
                placeholder="Місце події"
                icon={<MapPinIcon className="w-7"/>}
              />
              <FormField
                form={form}
                name="link"
                label="Посилання"
                placeholder="Посилання для події"
                icon={<LinkIcon className="w-7"/>}
              />
              <FormField
                form={form}
                name="image"
                label="Зображення"
                type="file"
                icon={<PhotoIcon className="w-7"/>}
              />
              {teamId && (
                <AssignToSelectField
                  form={form}
                  name="assigned_to_ids"
                  teamId={teamId}
                  label="Призначити подію"
                  placeholder="Оберіть кому призначити цю подію"
                />
              )}
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        
        <hr className="border-gray-300"/>
        
        <NotificationsFieldArray
          form={form}
          name="notifications"
        />
        <div className="flex justify-center">
          <Button
            type="submit"
            disabled={isLoading}
            className="text-md hover:cursor-pointer"
          >
            Додати подію
          </Button>
        </div>
      </FormBase>
    </div>
  )
}