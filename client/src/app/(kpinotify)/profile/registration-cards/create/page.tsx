import RegistrationCardForm from "@/components/forms/registrationCards/RegistrationCardForm";
import FormHeader from "@/components/forms/FormHeader";


export default function CreateRegistrationCardPage() {
  return (
    <div className="mx-auto max-w-4xl rounded-xl
     border border-sky-200 bg-white p-4 shadow-md"
    >
      <FormHeader
        title="Додайте реєстраційну картку АЦСК"
      />
      <RegistrationCardForm/>
    </div>
  )
}