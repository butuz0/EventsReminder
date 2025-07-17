"use client";

import FormBase from "@/components/forms/FormBase";
import {useSetupProfileMutation} from "@/lib/redux/slices/users/usersApiSlice";
import {useForm} from "react-hook-form";
import {toast} from "react-toastify";
import {useRouter} from "next/navigation";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import DepartmentSelectField from "@/components/forms/user/DepartmentSelectField";
import {zodResolver} from "@hookform/resolvers/zod";
import {ProfileSetupSchema, TProfileSetupSchema} from "@/lib/validationSchemas/ProfileSetupSchema";
import extractErrorMessage from "@/utils/extractErrorMessage";


export default function ProfileSetupForm() {
  const router = useRouter();
  
  const [updateProfileMutation, {isLoading}] = useSetupProfileMutation();
  const form = useForm<TProfileSetupSchema>({
    resolver: zodResolver(ProfileSetupSchema),
    mode: "all",
    defaultValues: {
      position: "",
      department: 0,
    },
  });
  
  const onSubmit = async (values: TProfileSetupSchema) => {
    try {
      await toast.promise(
        updateProfileMutation(values).unwrap(), {
          pending: "Оновлюємо ваш профіль...",
          success: "Ваш профіль успішно оновлено!"
        })
      router.push("/profile");
      form.reset();
    } catch (error) {
      toast.error(`При оновлені Вашого профілю сталась помилка: ${extractErrorMessage(error)}`)
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
        name="position"
        label="Посада"
        placeholder="Ваша посада"
      />
      <DepartmentSelectField
        form={form}
      />
      <div className="flex justify-center">
        <Button
          type="submit"
          disabled={isLoading}
          className="text-md hover:cursor-pointer"
        >
          Підтвердити
        </Button>
      </div>
    </FormBase>
  )
}