import * as z from "zod";

export const TeamSchema = z.object({
  name: z
    .string()
    .trim()
    .min(3, {message: "Назва команди має бути не меншою за 3 символи"})
    .max(100, {message: "Назва команди має бути не більшою за 100 символів"}),
  description: z
    .string()
    .trim()
    .max(250, {message: "Опис команди не може бути більшим за 250 символів"})
    .optional(),
  members_ids: z
    .array(
      z
        .string()
        .uuid()
    ).optional(),
});

export type TTeamSchema = z.infer<typeof TeamSchema>;
