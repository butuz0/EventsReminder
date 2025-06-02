import * as z from "zod";

export const PasswordResetRequestSchema = z.object({
  email: z
    .string()
    .trim()
    .email({message: "Введіть коректну електронну пошту"}),
});

export type TPasswordResetRequestSchema = z.infer<typeof PasswordResetRequestSchema>;