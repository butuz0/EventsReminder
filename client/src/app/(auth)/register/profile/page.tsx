import ProfileSetupForm from "@/components/forms/user/ProfileSetupForm";
import FormHeader from "@/components/forms/FormHeader";


export default function LoginPage() {
  return (
    <div className="w-full">
      <FormHeader
        title="Налаштування профілю"
        staticText="Додайте обов'язкову інформацію про себе"
      />
      <ProfileSetupForm/>
    </div>
  );
}