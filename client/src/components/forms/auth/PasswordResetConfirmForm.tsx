"use client";

import {useResetPasswordConfirmMutation} from "@/lib/redux/slices/auth/authApiSlice";
import {
  PasswordResetConfirmSchema,
  TPasswordResetConfirmSchema
} from "@/lib/validationSchemas/PasswordResetConfirmSchema";
import {useRouter} from "next/navigation";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "react-toastify";
import FormHeader from "@/components/forms/FormHeader";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {Button} from "@/components/ui/button";
import React from "react";
import extractErrorMessage from "@/utils/extractErrorMessage";

interface PasswordResetConfirmForm {
  uid: string,
  token: string
}


export default function PasswordResetConfirmForm({uid, token}: PasswordResetConfirmForm) {
  const router = useRouter();
  
  const [resetPasswordConfirm, {isLoading}] = useResetPasswordConfirmMutation();
  
  const form = useForm<TPasswordResetConfirmSchema>({
    mode: "all",
    resolver: zodResolver(PasswordResetConfirmSchema),
    defaultValues: {
      uid: uid,
      token: token,
      new_password: "",
      re_new_password: "",
    },
  });
  
  const onSubmit = async (values: TPasswordResetConfirmSchema) => {
    try {
      await resetPasswordConfirm(values).unwrap();
      toast.success("Ваш пароль було успішно оновлено");
      router.push("/login");
      form.reset();
    } catch (error) {
      toast.error(`При оновлені паролю сталась помилка: ${extractErrorMessage(error)}`)
    }
  };
  
  return (
    <div className="w-full">
      <FormHeader
        title="Оновлення паролю"
      />
      <FormBase
        form={form}
        onSubmit={onSubmit}
        className="w-full"
      >
        <FormField
          form={form}
          name="new_password"
          label="Новий пароль"
          placeholder="Ваш новий пароль"
          isPassword
        />
        <FormField
          form={form}
          name="re_new_password"
          label="Підтвердження паролю"
          placeholder="Повторіть ваш новий пароль"
          isPassword
        />
        <div className="flex justify-center">
          <Button
            type="submit"
            disabled={isLoading}
            className="text-md hover:cursor-pointer"
          >
            Оновити пароль
          </Button>
        </div>
      </FormBase>
    </div>
  );
}