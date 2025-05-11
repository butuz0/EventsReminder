import * as z from "zod";

export const ProfileSchema = z.object({
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
  position: z
    .string()
    .trim()
    .min(1, "Введіть свою посаду")
    .max(250, "Посада повинна мати не більше 250 символів"),
  phone_number: z.string().trim().optional(),
  telegram_username: z.string().trim().optional(),
  avatar: z.any().optional(),
  telegram_phone_number: z.string().trim().optional(),
  department: z
    .number()
    .refine((val) => val > 0, {message: "Оберіть свою кафедру",}),
  gender: z.enum(["m", "f", "o"]),
  
});

export type TProfileSchema = z.infer<typeof ProfileSchema>;
