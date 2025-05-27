import * as z from "zod";

export const UserLoginSchema = z.object({
  email: z
    .string()
    .trim()
    .email({message: "Введіть коректну електронну пошту"}),
  password: z
    .string()
    .trim()
    .min(6, {message: "Пароль має бути не меншим за 6 символів"}),
});

export type TUserLoginSchema = z.infer<typeof UserLoginSchema>;
