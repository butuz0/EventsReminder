import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import Select from "react-select";
import ClientOnlyComponent from "@/utils/ClientOnlyComponent";
import {
  FormLabel,
  FormControl,
  FormField,
  FormItem,
  FormMessage
} from "@/components/ui/form";
import React from "react";
import {selectFieldStyles} from "@/components/forms/selectFieldStyles";

type Option = {
  value: string | number;
  label: string
};

interface SelectFieldComponentProps<T extends FieldValues> {
  form: UseFormReturn<T>;
  name: Path<T>;
  label?: string;
  options: Option[];
  placeholder?: string;
  isDisabled?: boolean;
  isLoading?: boolean;
}


export default function SelectFieldComponent<T extends FieldValues>(
  {
    form,
    name,
    label,
    options,
    placeholder,
    isDisabled = false,
    isLoading = false,
  }: SelectFieldComponentProps<T>) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({field, fieldState}) => (
        <FormItem>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            <ClientOnlyComponent>
              <Select
                value={options.find((option) => option.value === field.value)}
                onChange={(selected) =>
                  field.onChange((selected as Option)?.value)
                }
                options={options}
                isDisabled={isDisabled}
                isLoading={isLoading}
                placeholder={placeholder}
                styles={selectFieldStyles}
                instanceId={name}
              />
            </ClientOnlyComponent>
          </FormControl>
          <FormMessage/>
        </FormItem>
      )}
    />
  );
}
