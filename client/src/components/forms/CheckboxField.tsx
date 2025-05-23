"use client";

import {
  FormControl,
  FormField as BaseFormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import React from "react";

type CheckboxFieldProps<T extends FieldValues> = {
  form: UseFormReturn<T>;
  name: Path<T>;
  label: string;
};


export default function CheckboxField<T extends FieldValues>(
  {
    form,
    name,
    label
  }: CheckboxFieldProps<T>) {
  return (
    <BaseFormField
      control={form.control}
      name={name}
      render={({field}) => (
        <FormItem className="flex items-center gap-3 space-y-0">
          <FormControl>
            <input
              type="checkbox"
              className="h-5 w-5 cursor-pointer rounded
              border-gray-300 text-sky-600 focus:ring-sky-500"
              checked={field.value}
              onChange={field.onChange}
            />
          </FormControl>
          <FormLabel className="text-sm font-medium leading-none">
            {label}
          </FormLabel>
          <FormMessage/>
        </FormItem>
      )}
    />
  );
}
