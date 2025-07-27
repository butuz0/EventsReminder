import * as z from "zod";

export const NotificationSchema = z.object({
  notification_method: z.enum(["email", "tg"], {
    message: "Оберіть метод нагадування"
  }),
  notification_datetime: z
    .coerce
    .date({message: "Оберіть дату та час нагадування"})
    .refine(
      (date) => date.getTime() >= Date.now(),
      {message: "Нагадування має бути у майбутньому"}
    ),
});

export type TNotificationSchema = z.infer<typeof NotificationSchema>;