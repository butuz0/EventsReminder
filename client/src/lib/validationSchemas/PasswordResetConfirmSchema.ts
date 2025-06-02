import * as z from "zod";

export const PasswordResetConfirmSchema = z.object({
  uid: z.string().trim(),
  token: z.string().trim(),
  new_password: z
    .string()
    .min(6, {message: "Пароль має бути не меншим за 6 символів"}),
  re_new_password: z
    .string()
    .min(6, {
      message: "Підтвердження паролю має бути не меншим за 6 символів",
    }),
}).refine((data) => data.new_password === data.re_new_password, {
  message: "Паролі не співпадають",
  path: ["re_new_password"],
});

export type TPasswordResetConfirmSchema = z.infer<typeof PasswordResetConfirmSchema>;
