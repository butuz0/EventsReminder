"use client";

import {
  FormControl,
  FormField as BaseFormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {Input} from "@/components/ui/input";
import {Textarea} from "@/components/ui/textarea";
import {PasswordInput} from "@/components/forms/PasswordInput";
import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import React from "react";


type FormFieldProps<T extends FieldValues> = {
  form: UseFormReturn<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
  isPassword?: boolean;
  isTextarea?: boolean;
  type?: React.HTMLInputTypeAttribute;
  icon?: React.ReactNode;
  className?: string;
  disabled?: boolean;
};


export default function FormField<T extends FieldValues>(
  {
    form,
    name,
    label,
    isPassword,
    isTextarea,
    placeholder,
    type = "text",
    icon,
    className,
    disabled,
  }: FormFieldProps<T>) {
  return (
    <BaseFormField
      control={form.control}
      name={name}
      render={({field}) => (
        <FormItem>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            <div className="flex w-full items-center gap-2">
              {icon}
              
              {isTextarea ? (
                <Textarea
                  {...field}
                  placeholder={placeholder}
                  className={className}
                />
              ) : isPassword ? (
                <PasswordInput
                  {...field}
                  placeholder={placeholder}
                  className={className}
                  disabled={disabled}
                />
              ) : type === "file" ? (
                <Input
                  type="file"
                  className={className}
                  disabled={disabled}
                  onChange={(e) => field.onChange(e.target.files?.[0])}
                />
              ) : (
                <Input
                  {...field}
                  placeholder={placeholder}
                  type={type}
                  className={className}
                  disabled={disabled}
                />
              )}
            </div>
          </FormControl>
          <FormMessage/>
        </FormItem>
      )}
    />
  );
}
