import {useGetAllProfilesQuery} from "@/lib/redux/slices/users/usersApiSlice";
import {Profile} from "@/types";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {FieldValues, Path, UseFormReturn} from "react-hook-form";

type UserOption = {
  label: string;
  value: string;
};


type MembersSelectFieldProps<T extends FieldValues> = {
  form: UseFormReturn<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
};

export default function MembersSelectField<T extends FieldValues>(
  {
    form,
    name,
    label,
    placeholder = "Оберіть користувачів"
  }: MembersSelectFieldProps<T>) {
  const {data, isLoading} = useGetAllProfilesQuery({});
  
  const getLabel = (profile: Profile) => {
    const name = `${profile.last_name} ${profile.first_name}`;
    const position = profile.position;
    const department = `${profile.department_name}, ${profile.faculty_abbreviation}`;
    return `${name} - ${position} | ${department}`;
  }
  
  const allOptions: UserOption[] =
    data?.profiles.results.map((profile) => ({
      label: getLabel(profile),
      value: profile.id,
    })) ?? [];
  
  const loadOptions = (inputValue: string, callback: (options: UserOption[]) => void) => {
    const filtered = allOptions.filter((option) =>
      option.label.toLowerCase().includes(inputValue.toLowerCase())
    );
    callback(filtered);
  };
  
  return (
    <SelectFieldComponent
      form={form}
      name={name}
      isMulti
      isAsync
      options={allOptions}
      loadOptions={loadOptions}
      isLoading={isLoading}
      isDisabled={isLoading}
      label={label}
      placeholder={placeholder}
    />
  )
}