"use client";

import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {TTeamSchema, TeamSchema} from "@/lib/validationSchemas/TeamSchema";
import {useGetTeamDetailsQuery, useUpdateTeamMutation} from "@/lib/redux/slices/teams/teamsApiSlice";
import {toast} from "react-toastify";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import extractErrorMessage from "@/utils/extractErrorMessage";

interface TeamUpdateFormProps {
  teamId: string;
}


export default function TeamUpdateForm({teamId}: TeamUpdateFormProps) {
  const {data, isLoading: isTeamLoading, isError} = useGetTeamDetailsQuery(teamId);
  const [updateTeam, {isLoading}] = useUpdateTeamMutation();
  const router = useRouter();
  
  const form = useForm<TTeamSchema>({
    resolver: zodResolver(TeamSchema),
    mode: "all",
    defaultValues: {
      name: data?.team.name,
      description: data?.team.description ?? ""
    },
  });
  
  if (isTeamLoading) {
    return <LoaderComponent
      size="lg"
      className="h-3/5"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити сторінку. Спробуйте ще раз.
      </div>
    )
  }
  
  const onSubmit = async (values: TTeamSchema) => {
    try {
      await toast.promise(
        updateTeam({teamId: data?.team.id, data: values}).unwrap(),
        {
          pending: "Змінюємо інформацію про команду...",
          success: "Команду успішно оновлено!"
        }
      );
      router.push(`/teams/${data?.team.id}`);
      form.reset();
    } catch (error) {
      toast.error(`При оновленні команди сталась помилка: ${extractErrorMessage(error)}`)
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
      <div className="flex justify-center">
        <Button
          disabled={isLoading}
          type="submit"
          className="text-md hover:cursor-pointer"
        >
          Оновити
        </Button>
      </div>
    </FormBase>
  )
}