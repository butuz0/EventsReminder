import * as z from "zod";

export const RegistrationCardSchema = z.object({
  organization_name: z
    .string()
    .trim()
    .min(1, "Введіть назву Організації"),
  edrpou_code: z
    .string()
    .trim()
    .regex(/^\d+$/, {message: "Код ЄДРПОУ має містити лише цифри"})
    .length(8, "Довжина коду ЄДРПОУ має становити 8 символів")
    .optional()
    .or(z.literal("")),
  region: z
    .string()
    .trim()
    .optional(),
  city: z
    .string()
    .trim()
    .optional(),
  full_name: z
    .string()
    .trim()
    .optional(),
  id_number: z
    .string()
    .trim()
    .regex(/^\d+$/, {message: "ID має містити лише цифри"})
    .optional()
    .or(z.literal("")),
  keyword_phrase: z
    .string()
    .trim()
    .optional(),
  voice_phrase: z
    .string()
    .trim()
    .optional(),
  email: z
    .string()
    .trim()
    .email()
    .optional()
    .or(z.literal("")),
  phone_number: z
    .string()
    .trim()
    .optional(),
  electronic_seal_name: z
    .string()
    .trim()
    .optional(),
  electronic_seal_keyword_phrase: z
    .string()
    .trim()
    .optional(),
});

export type TRegistrationCardSchema = z.infer<typeof RegistrationCardSchema>;