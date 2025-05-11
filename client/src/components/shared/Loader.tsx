"use client"

import {Loader2} from "lucide-react";
import React from "react";
import clsx from "clsx";

type LoaderSize = "sm" | "md" | "lg" | "xl";

interface LoaderComponentProps {
  text?: string
  size?: LoaderSize
  className?: string
}

const iconSize: Record<LoaderSize, string> = {
  sm: "w-4 h-4",
  md: "w-6 h-6",
  lg: "w-8 h-8",
  xl: "w-10 h-10",
};

const textSize: Record<LoaderSize, string> = {
  sm: "text-sm",
  md: "text-base",
  lg: "text-lg",
  xl: "text-xl",
};


export default function LoaderComponent(
  {
    text = "Завантаження...",
    size = "md",
    className = "",
  }: LoaderComponentProps) {
  return (
    <div className={clsx("flex items-center justify-center", className)}>
      <Loader2
        className={clsx("animate-spin text-gray-500", iconSize[size])}
      />
      <p className={clsx("ml-2 text-gray-600", textSize[size])}>
        {text}
      </p>
    </div>
  )
}