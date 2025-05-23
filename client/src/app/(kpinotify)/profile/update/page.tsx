import EditProfileForm from "@/components/forms/user/UpdateProfileForm";
import PageTitle from "@/components/shared/PageTitle";


export default function UpdateProfilePage() {
  return (
    <div className="mx-auto max-w-4xl">
      <PageTitle title="Оновіть свій профіль"/>
      <EditProfileForm/>
    </div>
  )
}