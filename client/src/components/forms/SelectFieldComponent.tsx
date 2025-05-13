import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import Select from "react-select";
import AsyncSelect from "react-select/async";
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
  options?: Option[];
  loadOptions?: (inputValue: string, callback: (options: Option[]) => void) => void;
  placeholder?: string;
  isDisabled?: boolean;
  isLoading?: boolean;
  isMulti?: boolean;
  isAsync?: boolean;
}


export default function SelectFieldComponent<T extends FieldValues>(
  {
    form,
    name,
    label,
    options,
    loadOptions,
    placeholder,
    isDisabled = false,
    isLoading = false,
    isMulti = false,
    isAsync = false,
  }: SelectFieldComponentProps<T>) {
  const SelectComponent = isAsync ? AsyncSelect : Select;
  
  return (
    <FormField
      control={form.control}
      name={name}
      render={({field}) => (
        <FormItem>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            {/*<ClientOnlyComponent>*/}
            <SelectComponent
              value={
                isMulti
                  ? options?.filter((option) => field.value?.includes(option.value))
                  : options?.find((option) => option.value === field.value)
              }
              onChange={(selected: any) => {
                if (isMulti) {
                  field.onChange((selected || []).map((s: Option) => s.value));
                } else {
                  field.onChange((selected as Option)?.value);
                }
              }}
              isMulti={isMulti}
              cacheOptions
              defaultOptions={options}
              loadOptions={loadOptions}
              options={options}
              isDisabled={isDisabled}
              isLoading={isLoading}
              placeholder={placeholder}
              styles={selectFieldStyles}
              instanceId={name}
            />
            {/*</ClientOnlyComponent>*/}
          </FormControl>
          <FormMessage/>
        </FormItem>
      )}
    />
  );
}
