"use client";

import {FieldValues, useFieldArray, UseFormReturn} from "react-hook-form";
import {Button} from "@/components/ui/button";
import FormField from "@/components/forms/FormField";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {NotificationMethods} from "@/constants";

interface NotificationFieldsGroupProps<T extends FieldValues> {
  form: UseFormReturn<T>;
  name: keyof T & string;
}


export default function NotificationsFieldArray<T extends FieldValues>(
  {
    form,
    name,
  }: NotificationFieldsGroupProps<T>) {
  const {fields, append, remove} = useFieldArray({
    control: form.control,
    name: name as any,
  });
  
  return (
    <div className="mt-6 space-y-4">
      <p className="text-lg font-medium">Нагадування</p>
      {fields.map((field, index) => (
        <div
          key={field.id}
          className="flex flex-col gap-3 rounded-md
          border border-gray-200 bg-white p-2"
        >
          <div className="flex flex-row gap-4">
            <FormField
              form={form}
              name={`${name}.${index}.notification_datetime` as any}
              type="datetime-local"
            />
            
            <SelectFieldComponent
              form={form}
              name={`${name}.${index}.notification_method` as any}
              options={NotificationMethods}
              placeholder="Метод нагадування"
            />
            <Button
              type="button"
              variant="secondary"
              className="border border-red-400 bg-red-100 text-red-600 hover:cursor-pointer hover:bg-red-200"
              onClick={() => remove(index)}
            >
              Видалити
            </Button>
          </div>
        </div>
      ))}
      <Button
        type="button"
        variant="secondary"
        className="border border-gray-300 shadow-md hover:cursor-pointer"
        onClick={() =>
          append({
            // @ts-ignore
            notification_datetime: undefined,
            notification_method: undefined,
          })
        }
      >
        Додати нагадування
      </Button>
    </div>
  );
}
