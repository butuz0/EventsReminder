import * as z from "zod";

export const RecurringEventSchema = z.object({
  recurrence_rule: z
    .string()
    .min(1, "Оберіть періодичність повторення"),
  recurrence_end_datetime: z
    .string()
    .refine(
      val => !isNaN(Date.parse(val)),
      {message: "Невірний формат дати завершення повторюваності"}
    )
});

export type TRecurringEventSchema = z.infer<typeof RecurringEventSchema>;
