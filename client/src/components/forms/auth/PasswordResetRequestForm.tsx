"use client";

import {zodResolver} from "@hookform/resolvers/zod";
import {useResetPasswordRequestMutation} from "@/lib/redux/slices/auth/authApiSlice";
import FormField from "@/components/forms/FormField";
import {useForm} from "react-hook-form";
import {toast} from "react-toastify";
import {Button} from "@/components/ui/button";
import {
  PasswordResetRequestSchema,
  TPasswordResetRequestSchema
} from "@/lib/validationSchemas/PasswordResetRequestSchema";
import FormHeader from "@/components/forms/FormHeader";
import FormBase from "@/components/forms/FormBase";
import {AtSymbolIcon,} from "@heroicons/react/24/outline";
import React from "react";
import extractErrorMessage from "@/utils/extractErrorMessage";


export default function PasswordResetRequestForm() {
  const [resetPasswordRequest, {isLoading}] = useResetPasswordRequestMutation();
  
  const form = useForm<TPasswordResetRequestSchema>({
    resolver: zodResolver(PasswordResetRequestSchema),
    mode: "all",
    defaultValues: {
      email: "",
    },
  });
  
  const onSubmit = async (values: TPasswordResetRequestSchema) => {
    try {
      await resetPasswordRequest(values).unwrap();
      toast.success(`На електронну пошту ${values.email} було надіслано лист із посиланням для оновлення паролю`);
      form.reset();
    } catch (error) {
      toast.error(`При надсиланні запиту на зміну паролю сталась помилка: ${extractErrorMessage(error)}`)
    }
  };
  
  return (
    <div className="w-full">
      <FormHeader
        title="Запит на зміну паролю"
        linkText="До сторінки входу"
        linkHref="/login"
      />
      <FormBase
        form={form}
        onSubmit={onSubmit}
        className="w-full"
      >
        <FormField
          form={form}
          name="email"
          label="Електронна пошта"
          placeholder="Email @kpi.ua"
          type="email"
          icon={<AtSymbolIcon className="w-7"/>}
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
    </div>
  );
}