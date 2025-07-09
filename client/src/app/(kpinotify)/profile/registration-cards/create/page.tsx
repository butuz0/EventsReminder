import RegistrationCardForm from "@/components/forms/registrationCards/RegistrationCardForm";
import FormHeader from "@/components/forms/FormHeader";
import PageTitle from "@/components/shared/PageTitle";


export default function CreateRegistrationCardPage() {
  return (
    <div>
      <PageTitle title="Додайте картку АЦСК"/>
      <div className="mx-auto max-w-4xl rounded-xl
     border border-sky-200 bg-white p-4 shadow-md"
      >
        <FormHeader
          title="Додайте нову реєстраційну картку АЦСК"
        />
        <RegistrationCardForm/>
      </div>
    </div>
  )
}