import * as z from "zod";

export const DeleteAccountSchema = z.object({
  current_password: z
    .string()
    .trim()
    .min(6, {message: "Пароль має бути не меншим за 6 символів"}),
});

export type TDeleteAccountSchema = z.infer<typeof DeleteAccountSchema>;
