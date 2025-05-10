"use client"

import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";
import {toast} from "react-toastify";
import {Button} from "@/components/ui/button"
import {TUserLoginSchema, UserLoginSchema} from "@/lib/validationSchemas/LoginSchema";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {AtSymbolIcon} from "@heroicons/react/24/outline";
import {useLoginUserMutation} from "@/lib/redux/slices/auth/authApiSlice";


export default function LoginForm() {
  const [loginUser, {isLoading}] = useLoginUserMutation();
  
  const form = useForm<TUserLoginSchema>({
    resolver: zodResolver(UserLoginSchema),
    mode: "all",
    defaultValues: {
      email: "",
      password: "",
    },
  })
  
  const onSubmit = async (values: TUserLoginSchema) => {
    try {
      await toast.promise(
        loginUser(values).unwrap(),
        {
          pending: "Ваші дані обробляються...",
          success: "Ви успішно увійшли в свій акаунт",
        }
      );
    } catch (error) {
      toast.error(`При створенні Вашого акаунта сталась помилка: ${JSON.stringify(error)}`)
    }
  };
  return (
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
      <FormField
        form={form}
        name="password"
        label="Пароль"
        placeholder="Ваш пароль"
        isPassword
      />
      <div className="flex justify-center">
        <Button
          type="submit"
          disabled={isLoading}
          className="w-1/4 text-md hover:cursor-pointer"
        >
          Вхід
        </Button>
      </div>
    </FormBase>
  )
}
