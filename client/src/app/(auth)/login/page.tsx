import FormHeader from "@/components/forms/FormHeader";
import LoginForm from "@/components/forms/auth/LoginForm";


export default function LoginPage() {
  return (
    <div className="w-full">
      <FormHeader
        title="Вхід в акаунт"
        staticText="Ще не маєте акаунта?"
        linkText="Реєстрація"
        linkHref={"/register"}
      />
      <LoginForm/>
    </div>
  );
}