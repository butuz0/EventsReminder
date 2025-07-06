"use client";

import FormHeader from "@/components/forms/FormHeader";
import LoginForm from "@/components/forms/auth/LoginForm";
import useRedirectIfAuthenticated from "@/hooks/useRedirectIfAuthenticated";


export default function LoginPage() {
  useRedirectIfAuthenticated();
  
  return (
    <div className="w-full">
      <FormHeader
        title="Вхід в акаунт"
        staticText="Ще не маєте акаунту?"
        linkText="Реєстрація"
        linkHref="/register"
      />
      <LoginForm/>
    </div>
  );
}