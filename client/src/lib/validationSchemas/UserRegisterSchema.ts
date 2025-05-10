import * as z from "zod";

export const UserRegisterSchema = z.object({
  email: z
    .string()
    .trim()
    .email({message: "Введіть коректну електронну пошту"})
    .endsWith("@kpi.ua", "Ви можете зареєструватись лише через корпоративну пошту @kpi.ua"),
  first_name: z
    .string()
    .trim()
    .min(2, {message: "Ім'я має бути не меншим за 2 символи"})
    .max(50, {message: "Ім'я має бути не більшим за 50 символів"}),
  last_name: z
    .string()
    .trim()
    .min(2, {message: "Прізвище має бути не меншим за 2 символи"})
    .max(50, {message: "Прізвище має бути не більшим за 50 символів"}),
  password: z
    .string()
    .min(6, {message: "Пароль має бути не меншим за 6 символів"}),
  re_password: z
    .string()
    .min(6, {
      message: "Підтвердження паролю має бути не меншим за 6 символів",
    }),
}).refine((data) => data.password === data.re_password, {
  message: "Паролі не співпадають",
  path: ["re_password"],
});

export type TUserRegisterSchema = z.infer<typeof UserRegisterSchema>;
