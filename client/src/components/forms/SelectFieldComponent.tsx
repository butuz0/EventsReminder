import {Controller, FieldValues, Path, UseFormReturn} from "react-hook-form";
import Select from "react-select";
import ClientOnlyComponent from "@/utils/ClientOnlyComponent";
import {FormLabel} from "@/components/ui/form";
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
    <div className="space-y-1">
      {label && <FormLabel>{label}</FormLabel>}
      <ClientOnlyComponent>
        <Controller
          control={form.control}
          name={name}
          render={({field}) => (
            <Select
              {...field}
              options={options}
              isDisabled={isDisabled}
              isLoading={isLoading}
              onChange={(selected) => field.onChange((selected as Option)?.value)}
              value={options.find((option) => option.value === field.value)}
              placeholder={placeholder}
              styles={selectFieldStyles}
            />
          )}
        />
      </ClientOnlyComponent>
    </div>
  );
}
