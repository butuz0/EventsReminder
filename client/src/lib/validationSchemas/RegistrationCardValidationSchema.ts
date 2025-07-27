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
    .union([
      z.string().trim().regex(/^\+380\d{9}$/, "Номер телефону повинен мати формат '+380xxxxxxxxx'"),
      z.literal(""),
    ])
    .optional(),
  electronic_seal_name: z
    .string()
    .trim()
    .optional(),
  electronic_seal_keyword_phrase: z
    .string()
    .trim()
    .optional(),
  issue_date: z
    .string()
    .refine(val => !isNaN(Date.parse(val)), {
      message: "Невірний формат дати",
    }),
  expiration_date: z
    .string()
    .refine(val => !isNaN(Date.parse(val)), {
      message: "Невірний формат дати",
    }),
}).refine((data) => {
    if (data.issue_date && data.expiration_date) {
      return data.expiration_date > data.issue_date;
    }
    return true;
  },
  {
    message: "Дата закінчення дії повинна бути пізніше за дату видачі",
    path: ["expiration_date"],
  }
);

export type TRegistrationCardSchema = z.infer<typeof RegistrationCardSchema>;