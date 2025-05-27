"use client";

import DeletionDialog from "@/components/shared/DeletionDialog";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {TDeleteAccountSchema, DeleteAccountSchema} from "@/lib/validationSchemas/DeleteAccoutSchema";
import FormField from "@/components/forms/FormField";
import {useDeleteCurrentUserMutation} from "@/lib/redux/slices/auth/authApiSlice";
import {toast} from "react-toastify";
import {useRouter} from "next/navigation";
import FormBase from "@/components/forms/FormBase";


export default function AccountDeleteButton() {
  const [deleteCurrentUser] = useDeleteCurrentUserMutation();
  const router = useRouter();
  
  const form = useForm<TDeleteAccountSchema>({
      resolver: zodResolver(DeleteAccountSchema),
      mode: "all",
      defaultValues: {
        current_password: ""
      }
    }
  );
  
  const onSubmit = async () => {
    const {current_password} = form.getValues();
    
    try {
      await toast.promise(deleteCurrentUser(current_password).unwrap(), {
        pending: "Видаляємо Ваш акаунт...",
        success: "Ваш акаунт було видалено"
      });
      router.push("/");
    } catch (error) {
      toast.error("При видаленні Вашого акаунту сталась помилка");
    }
  }
  
  return (
    <DeletionDialog
      buttonText="Видалити акаунт"
      confirmButtonText="Видалити акаунт"
      description="Цю дію неможливо скасувати. Видалення акаунту призведе до повного видалення усіх Ваших даних у застосунку."
      onConfirmAction={form.handleSubmit(onSubmit)}
    >
      <FormBase
        form={form}
        className="w-full"
      >
        <FormField
          form={form}
          name="current_password"
          label="Пароль"
          placeholder="Ваш пароль"
          isPassword
        />
      </FormBase>
    </DeletionDialog>
  )
}