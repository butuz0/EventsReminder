import ProfileSetupForm from "@/components/forms/user/ProfileSetupForm";
import FormHeader from "@/components/forms/FormHeader";


export default function ProfileSetupPage() {
  return (
    <div className="w-full">
      <FormHeader
        title="Налаштування профілю"
      />
      <ProfileSetupForm/>
    </div>
  );
}