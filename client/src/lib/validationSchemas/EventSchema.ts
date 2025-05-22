import * as z from "zod";
import {NotificationSchema} from "@/lib/validationSchemas/NotificationSchema";

export const EventSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, "Введіть назву події"),
  description: z
    .string()
    .trim()
    .optional(),
  start_datetime: z
    .string()
    .refine(val => !isNaN(Date.parse(val)), {
      message: "Невірний формат дати",
    })
    .refine(val => new Date(val).getTime() >= Date.now(), {
      message: "Подія має бути у майбутньому",
    }),
  location: z
    .string()
    .trim()
    .max(250, "Адреса має містити не більше 250 символів")
    .optional(),
  link: z
    .string()
    .trim()
    .url("Введені Вами дані не є посиланням")
    .optional(),
  priority: z
    .number()
    .int()
    .min(1, "Оберіть коректний пріоритет події")
    .max(4, "Оберіть коректний пріоритет події"),
  image: z.any().optional(),
  tags: z
    .array(
      z.string()
        .trim()
        .max(30, "Тег повинен містити не більше 30 символів")
    )
    .optional(),
  team: z
    .string()
    .uuid()
    .optional(),
  assigned_to_ids: z
    .array(
      z.string()
        .trim()
        .uuid("Обрано неіснуючого підлеглого")
    ).optional(),
  is_recurring: z.boolean().optional(),
});

export const EventWithNotificationsSchema = EventSchema.extend({
  notifications: z
    .array(NotificationSchema)
});

export type TEventSchema = z.infer<typeof EventSchema>;
export type TEventWithNotificationsSchema = z.infer<typeof EventWithNotificationsSchema>;
