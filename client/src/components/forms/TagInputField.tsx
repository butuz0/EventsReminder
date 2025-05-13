"use client";

import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {WithContext as ReactTags} from "react-tag-input";
import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import React from "react";


type TagInputFieldProps<T extends FieldValues> = {
  form: UseFormReturn<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
};

const KeyCodes = {
  enter: 13,
};

const delimiters = [KeyCodes.enter];


export default function TagInputField<T extends FieldValues>(
  {
    form,
    name,
    label,
    placeholder = "Додайте тег...",
  }: TagInputFieldProps<T>) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({field}) => (
        <FormItem>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            <ReactTags
              tags={(field.value || []).map((tag: string) => ({
                id: tag,
                text: tag,
                className: ""
              }))}
              handleDelete={(index) => {
                const newTags = [...(field.value || [])];
                newTags.splice(index, 1);
                field.onChange(newTags);
              }}
              handleAddition={(tag) => {
                const newTags = [...(field.value || []), tag.text];
                field.onChange(newTags);
              }}
              delimiters={delimiters}
              placeholder={placeholder}
              inputFieldPosition="inline"
              allowDragDrop={false}
              maxTags={8}
              classNames={{
                tags: "border border-gray-200 rounded-md p-2 min-h-[3rem] bg-white text-sm",
                tag: "bg-sky-100 text-blue-900 border border-blue-900 rounded px-2 py-1 mx-1",
                remove: "cursor-pointer ml-2",
                tagInputField: "outline-none text-sm px-1 pt-3 w-full",
              }}
            />
          </FormControl>
          <FormMessage/>
        </FormItem>
      )}
    />
  );
}
