"use client"

import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";
import {toast} from "react-toastify";
import {Button} from "@/components/ui/button"
import {TUserRegisterSchema, UserRegisterSchema} from "@/lib/validationSchemas/UserRegisterSchema";
import FormBase from "@/components/forms/FormBase";
import FormField from "@/components/forms/FormField";
import {AtSymbolIcon, UserCircleIcon} from "@heroicons/react/24/outline";
import {useRegisterUserMutation} from "@/lib/redux/slices/auth/authApiSlice";
import extractErrorMessage from "@/utils/extractErrorMessage";


export default function UserRegisterForm() {
  const [registerUser, {isLoading}] = useRegisterUserMutation();
  
  const form = useForm<TUserRegisterSchema>({
    resolver: zodResolver(UserRegisterSchema),
    mode: "all",
    defaultValues: {
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      re_password: ""
    },
  })
  
  const onSubmit = async (values: TUserRegisterSchema) => {
    try {
      await toast.promise(
        registerUser(values).unwrap(),
        {
          pending: "Ваші дані обробляються...",
          success: "На Вашу електронну пошту надійшов лист для підтвердження створення акаунта.",
        }
      );
    } catch (error) {
      toast.error(`При створенні Вашого акаунта сталась помилка: ${extractErrorMessage(error)}`)
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
        name="first_name"
        label="Ім'я"
        placeholder="Ваше ім'я"
        icon={<UserCircleIcon className="w-7"/>}
      />
      <FormField
        form={form}
        name="last_name"
        label="Прізвище"
        placeholder="Ваше прізвище"
        icon={<UserCircleIcon className="w-7"/>}
      />
      <FormField
        form={form}
        name="password"
        label="Пароль"
        placeholder="Ваш пароль"
        isPassword
      />
      <FormField
        form={form}
        name="re_password"
        label="Підтвердження паролю"
        placeholder="Повторіть ваш пароль"
        isPassword
      />
      <div className="flex justify-center">
        <Button
          disabled={isLoading}
          type="submit"
          className="text-md hover:cursor-pointer"
        >
          Реєстрація
        </Button>
      </div>
    </FormBase>
  )
}
