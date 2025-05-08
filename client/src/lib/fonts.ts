import {Source_Serif_4, Nunito} from "next/font/google";

export const sourceSerif = Source_Serif_4({
  subsets: ["latin", "cyrillic"],
  variable: "--font-sourceSerif",
});

export const nunito = Nunito({
  subsets: ["latin", "cyrillic"],
  variable: "--font-nunito",
});