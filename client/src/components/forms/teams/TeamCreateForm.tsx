"use client";

import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {TTeamSchema, TeamSchema} from "@/lib/validationSchemas/TeamSchema";
import {useCreateTeamMutation} from "@/lib/redux/slices/teams/teamsApiSlice";
import {toast} from "react-toastify";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import MembersSelectField from "@/components/forms/teams/MembersSelectField";


export default function TeamCreateForm() {
  const [createTeam, {isLoading}] = useCreateTeamMutation();
  const router = useRouter();
  
  const form = useForm<TTeamSchema>({
    resolver: zodResolver(TeamSchema),
    mode: "all",
    defaultValues: {
      name: "",
      description: "",
      members_ids: []
    },
  })
  
  const onSubmit = async (values: TTeamSchema) => {
    try {
      await toast.promise(
        createTeam(values).unwrap(),
        {
          pending: "Створюємо команду...",
          success: `Команду успішно створено!
          ${values.members_ids && values.members_ids.length > 0
            ? "Користувачам було надіслано запрошення на електронну пошту."
            : ""}`
        }
      ).then((response) => {
        router.push(`/teams/${response.team.id}`);
        form.reset();
      });
    } catch (error) {
      toast.error(`При створенні команди сталась помилка: ${JSON.stringify(error)}`)
    }
  }
  
  return (
    <FormBase
      form={form}
      onSubmit={onSubmit}
      className="w-full"
    >
      <FormField
        form={form}
        name="name"
        label="Назва"
        placeholder="Введіть назву команди"
      />
      <FormField
        form={form}
        name="description"
        label="Опис команди"
        placeholder="Введіть опис команди"
        isTextarea
      />
      <MembersSelectField
        form={form}
        name="members_ids"
        label="Учасники"
        placeholder="Введіть ім'я учасника команди"
      />
      <div className="flex justify-center">
        <Button
          disabled={isLoading}
          type="submit"
          className="text-md hover:cursor-pointer"
        >
          Створити команду
        </Button>
      </div>
    </FormBase>
  )
}