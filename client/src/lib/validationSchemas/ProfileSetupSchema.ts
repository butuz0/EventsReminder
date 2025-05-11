import * as z from "zod";

export const ProfileSetupSchema = z.object({
  position: z
    .string()
    .trim()
    .min(1, "Введіть свою посаду")
    .max(250, "Посада повинна мати не більше 250 символів"),
  department: z
    .number()
    .refine((val) => val > 0, {message: "Оберіть свою кафедру"}),
  gender: z.enum(["m", "f", "o"], {message: "Оберіть свою стать"}),
});

export type TProfileSetupSchema = z.infer<typeof ProfileSetupSchema>;
