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
  avatar: z.any().optional(),
  department: z
    .number()
    .refine((val) => val > 0, {message: "Оберіть свою кафедру",}),
});

export type TProfileSchema = z.infer<typeof ProfileSchema>;
