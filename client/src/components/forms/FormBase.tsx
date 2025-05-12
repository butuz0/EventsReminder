import {Form} from "@/components/ui/form";
import {UseFormReturn} from "react-hook-form";
import React from "react";

interface FormBaseProps extends React.FormHTMLAttributes<HTMLFormElement> {
  form: UseFormReturn<any>;
  onSubmit: (data: any) => void;
  className?: string;
  children?: React.ReactNode;
}


export default function FormBase(
  {
    form,
    onSubmit,
    className = "",
    children
    , ...rest
  }: FormBaseProps) {
  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={`space-y-5 ${className}`}
        {...rest}
      >
        {children}
      </form>
    </Form>
  )
}
