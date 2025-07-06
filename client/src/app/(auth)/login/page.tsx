import FormHeader from "@/components/forms/FormHeader";
import LoginForm from "@/components/forms/auth/LoginForm";
import {Metadata} from "next";

export const metadata: Metadata = {
  title: "KPI Notify | Log In"
}


export default function LoginPage() {
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