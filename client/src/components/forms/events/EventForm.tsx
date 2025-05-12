"use client";

import FormBase from "@/components/forms/FormBase";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {PriorityOptions} from "@/constants";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "react-toastify";
import {useCreateEventMutation} from "@/lib/redux/slices/events/eventsApiSlice";
import {useCreateNotificationMutation} from "@/lib/redux/slices/notifications/notificationsApiSlice";
import {
  EventWithNotificationsSchema,
  TEventWithNotificationsSchema
} from "@/lib/validationSchemas/EventSchema";
import {MapPinIcon, CalendarIcon, PhotoIcon, LinkIcon, ClipboardDocumentListIcon} from "@heroicons/react/24/outline";
import FormHeader from "@/components/forms/FormHeader";
import objToFormData from "@/utils/objToFormData";
import TagInputField from "@/components/forms/TagInputField";
import NotificationsFieldArray from "@/components/forms/events/NotificationsFieldArray";


export default function EventForm() {
  const router = useRouter();
  
  const [createEvent, {isLoading}] = useCreateEventMutation();
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
      assigned_to: [],
      is_recurring: false,
      notifications: []
    },
  });
  
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
          pending: "Створюємо подію...",
          success: "Подію створено",
        }
      );
      
      // create notifications for a new event
      if (notifications.length > 0) {
        await Promise.all(
          notifications.map((n) =>
            createNotification({
              ...n,
              event: response.event.id,
            }).unwrap()
          )
        );
        toast.success("Нагадування створено");
      }
      
      router.push(`/events/${response.event.id}`);
      form.reset();
    } catch (error) {
      toast.error("При створенні події сталась помилка.")
    }
  }
  
  return (
    <div className="w-full max-w-3xl bg-white p-5 rounded-xl
    border border-sky-200 shadow-md flex flex-col justify-center">
      <FormHeader
        title="Створіть нову подію"
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
          name="description"
          label="Опис"
          placeholder="Додатковий опис події"
          isTextarea
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
            Підтвердити
          </Button>
        </div>
      </FormBase>
    </div>
  )
}