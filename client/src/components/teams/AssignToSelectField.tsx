import {BaseUserResponse} from "@/types";
import SelectFieldComponent from "@/components/forms/SelectFieldComponent";
import {FieldValues, Path, UseFormReturn} from "react-hook-form";
import {useGetTeamMembersQuery} from "@/lib/redux/slices/teams/teamsApiSlice";

type UserOption = {
  label: string;
  value: string;
};


type MembersSelectFieldProps<T extends FieldValues> = {
  form: UseFormReturn<T>;
  name: Path<T>;
  teamId: string;
  label?: string;
  placeholder?: string;
};

export default function MembersSelectField<T extends FieldValues>(
  {
    form,
    name,
    teamId,
    label,
    placeholder = "Оберіть користувачів"
  }: MembersSelectFieldProps<T>) {
  const {data, isLoading} = useGetTeamMembersQuery(teamId);
  const teamMembers = data?.results;
  
  const getLabel = (member: BaseUserResponse) => {
    return `${member.last_name} ${member.first_name}`;
  }
  
  const allOptions: UserOption[] =
    teamMembers?.map((member) => ({
      label: getLabel(member),
      value: member.id,
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