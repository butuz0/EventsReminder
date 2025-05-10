import UserRegisterForm from "@/components/forms/auth/UserRegisterForm";
import FormHeader from "@/components/forms/FormHeader";


export default function RegisterPage() {
  return (
    <div className="w-full">
      <FormHeader
        title="Створіть новий акаунт"
        staticText="Вже зареєстровані?"
        linkText="Увійти в акаунт"
        linkHref={"/login"}
      />
      <UserRegisterForm/>
    </div>
  );
}
