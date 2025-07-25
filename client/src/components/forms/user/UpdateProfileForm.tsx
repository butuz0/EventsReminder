"use client";

import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import React from "react";
import {toast} from "react-toastify";
import {useGetMyProfileQuery, useUpdateProfileMutation} from "@/lib/redux/slices/users/usersApiSlice";
import {ProfileSchema, TProfileSchema} from "@/lib/validationSchemas/ProfileSchema";
import {Button} from "@/components/ui/button";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import DepartmentSelectField from "@/components/forms/user/DepartmentSelectField";
import objToFormData from "@/utils/objToFormData";
import LoaderComponent from "@/components/shared/Loader";
import FormHeader from "@/components/forms/FormHeader";
import {useRouter} from "next/navigation";
import extractErrorMessage from "@/utils/extractErrorMessage";


export default function EditProfileForm() {
  const router = useRouter();
  const {data, isLoading, isError} = useGetMyProfileQuery();
  const [updateProfile, {isLoading: isUpdating}] = useUpdateProfileMutation();
  
  const form = useForm<TProfileSchema>({
    resolver: zodResolver(ProfileSchema),
    mode: "onChange",
    defaultValues: {
      first_name: data?.profile.first_name ?? "",
      last_name: data?.profile.last_name ?? "",
      position: data?.profile.position ?? "",
      avatar: undefined,
      department: Number(data?.profile.department) ?? undefined,
    },
  });
  
  if (isLoading) {
    return <LoaderComponent
      size="xl"
      text="Завантаження профілю..."
      className="h-3/4"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center font-medium text-red-600">
        Не вдалося завантажити профіль. Спробуйте ще раз.
      </div>
    )
  }
  
  const onSubmit = async (values: TProfileSchema) => {
    try {
      const hasImage = values.avatar instanceof File;
      const data = hasImage
        ? objToFormData(values)
        : values;
      
      await toast.promise(updateProfile(data).unwrap(), {
        pending: "Оновлюємо профіль...",
        success: "Профіль оновлено!"
      });
      router.push("/profile");
    } catch (error) {
      toast.error(`При оновлені Вашого профілю сталась помилка: ${extractErrorMessage(error)}`)
    }
  };
  
  return (
    <div className="w-full rounded-xl border border-sky-200
    bg-white shadow-md p-4">
      <FormHeader
        linkText="Назад до профілю"
        linkHref="/profile"
      />
      <FormBase
        form={form}
        onSubmit={onSubmit}
        encType="multipart/form-data"
      >
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <FormField
            form={form}
            name="first_name"
            label="Ім’я"
          />
          <FormField
            form={form}
            name="last_name"
            label="Прізвище"
          />
          <FormField
            form={form}
            name="position"
            label="Посада"
          />
          <FormField
            form={form}
            name="avatar"
            label="Аватар"
            type="file"
          />
        </div>
        
        <div className="mt-6">
          <DepartmentSelectField form={form}/>
        </div>
        
        <div className="mt-8 flex justify-center">
          <Button
            type="submit"
            disabled={isUpdating}
            className="hover:cursor-pointer"
          >
            Зберегти зміни
          </Button>
        </div>
      </FormBase>
    </div>
  );
}
