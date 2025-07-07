"use client";

import FormBase from "@/components/forms/FormBase";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {PriorityOptions, RecurrenceRuleOptions} from "@/constants";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "react-toastify";
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
import AssignToSelectField from "@/components/teams/AssignToSelectField";
import {
  useCreateRecurringEventMutation,
  useUpdateEventMutation,
  useUpdateRecurringEventMutation
} from "@/lib/redux/slices/events/eventsApiSlice";
import {TEventSchema, EventSchema} from "@/lib/validationSchemas/EventSchema";
import {Event} from "@/types";
import {RecurringEventSchema, TRecurringEventSchema} from "@/lib/validationSchemas/RecurringEventSchema";
import CheckboxField from "@/components/forms/CheckboxField";

interface EventUpdateFormProps {
  event: Event;
}


export default function EventUpdateForm({event}: EventUpdateFormProps) {
  const router = useRouter();
  const [updateEvent, {isLoading}] = useUpdateEventMutation();
  const [createRecurringEvent] = useCreateRecurringEventMutation();
  const [updateRecurringEvent] = useUpdateRecurringEventMutation();
  
  const form = useForm<TEventSchema>({
    resolver: zodResolver(EventSchema),
    mode: "all",
    defaultValues: {
      title: event.title,
      description: event.description ?? undefined,
      start_datetime: event.start_datetime.slice(0, 16),
      location: event.location ?? undefined,
      link: event.link ?? undefined,
      priority: event.priority,
      image: undefined,
      tags: event.tags,
      team: event.team?.id,
      assigned_to_ids: event.assigned_to.map((user) => user.id),
      is_recurring: event.is_recurring,
    }
  });
  
  const recurringForm = useForm<TRecurringEventSchema>({
    resolver: zodResolver(RecurringEventSchema),
    mode: "all",
    defaultValues: {
      recurrence_rule: event.recurring_event?.recurrence_rule ?? "w",
      recurrence_end_datetime: event.recurring_event?.recurrence_end_datetime?.slice(0, 16) ?? undefined,
    }
  })
  
  const eventAlreadyRecurring = event.recurring_event !== null;
  
  const isRecurring = form.watch("is_recurring");
  
  const onSubmit = async (values: TEventSchema) => {
    try {
      const hasImage = values.image instanceof File;
      const data = hasImage
        ? objToFormData(values)
        : values;
      
      await toast.promise(
        updateEvent({event_id: event.id, data: data}).unwrap(),
        {
          pending: "Оновлення події...",
        }
      );
      
      if (isRecurring && eventAlreadyRecurring) {
        await updateRecurringEvent({event_id: event.id, data: recurringForm.getValues()}).unwrap();
      } else if (isRecurring && !eventAlreadyRecurring) {
        await createRecurringEvent({event_id: event.id, data: recurringForm.getValues()}).unwrap();
      }
      
      toast.success("Подію оновлено!");
      
      
      router.push(`/events/${event.id}`);
    } catch (err) {
      toast.error("Помилка під час оновлення події.");
    }
  };
  
  return (
    <div className="w-full bg-white p-5 rounded-xl
    border border-sky-200 shadow-md flex flex-col justify-center">
      <FormHeader title="Оновіть подію"/>
      
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
          placeholder="Введіть нову назву"
          icon={<ClipboardDocumentListIcon className="w-7"/>}
        />
        
        <FormField
          form={form}
          name="description"
          label="Опис"
          placeholder="Оновлений опис події"
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
          placeholder="Оберіть новий пріоритет"
          icon={<ExclamationCircleIcon className="w-7"/>}
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
          placeholder="Оновлене місце"
          icon={<MapPinIcon className="w-7"/>}
        />
        
        <FormField
          form={form}
          name="link"
          label="Посилання"
          placeholder="Оновлене посилання"
          icon={<LinkIcon className="w-7"/>}
        />
        
        <FormField
          form={form}
          name="image"
          label="Зображення"
          type="file"
          icon={<PhotoIcon className="w-7"/>}
        />
        
        {event.team && (
          <AssignToSelectField
            form={form}
            name="assigned_to_ids"
            teamId={event.team.id}
            label="Призначити"
            placeholder="Оновіть призначення"
          />
        )}
        
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
            />
          </div>
        )}
        
        <div className="flex justify-center">
          <Button
            type="submit"
            disabled={isLoading}
            className="text-md hover:cursor-pointer"
          >
            Зберегти зміни
          </Button>
        </div>
      </FormBase>
    </div>
  );
}
