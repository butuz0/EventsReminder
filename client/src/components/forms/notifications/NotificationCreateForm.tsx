"use client";

import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {NotificationSchema, TNotificationSchema} from "@/lib/validationSchemas/NotificationSchema";
import {useCreateNotificationMutation} from "@/lib/redux/slices/notifications/notificationsApiSlice";
import {Button} from "@/components/ui/button";
import FormField from "@/components/forms/FormField";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {NotificationMethods} from "@/constants";
import {toast} from "react-toastify";
import FormBase from "@/components/forms/FormBase";
import extractErrorMessage from "@/utils/extractErrorMessage";

interface NotificationCreateFormProps {
  eventId: string;
  onSuccess?: () => void;
}

export default function NotificationCreateForm(
  {
    eventId,
    onSuccess,
  }: NotificationCreateFormProps) {
  const [createNotification, {isLoading}] = useCreateNotificationMutation();
  
  const form = useForm<TNotificationSchema>({
    resolver: zodResolver(NotificationSchema),
    defaultValues: {
      event: eventId,
      notification_datetime: undefined,
      notification_method: undefined,
    },
  });
  
  const onSubmit = async (values: TNotificationSchema) => {
    try {
      // @ts-ignore
      await createNotification(values).unwrap();
      toast.success("Нагадування створено");
      form.reset({
        event: eventId,
        notification_datetime: new Date(),
        notification_method: "email",
      });
      onSuccess?.();
    } catch (error){
      toast.error(`Не вдалося створити нагадування: ${extractErrorMessage(error)}`)
    }
  };
  
  return (
    <FormBase
      form={form}
      onSubmit={onSubmit}
      className="space-y-4"
    >
      <div className="grid md:grid-cols-[3fr_2fr_auto] gap-4 items-end">
        <FormField
          form={form}
          name="notification_datetime"
          type="datetime-local"
          label=""
        />
        <SelectFieldComponent
          form={form}
          name="notification_method"
          options={NotificationMethods}
          placeholder="Метод нагадування"
          label=""
        />
        <Button
          type="submit"
          disabled={isLoading}
          className="w-1/6 md:w-auto"
        >
          Додати
        </Button>
      </div>
    </FormBase>
  );
}
