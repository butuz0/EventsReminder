import TeamCreateForm from "@/components/forms/teams/TeamCreateForm";
import FormHeader from "@/components/forms/FormHeader";
import PageTitle from "@/components/shared/PageTitle";


export default function CreateEventPage() {
  return (
    <div>
      <PageTitle title="Створіть нову команду"/>
      <div className="w-full flex justify-center">
        <div className="w-full max-w-3xl bg-white rounded-xl
        shadow-md p-4 border border-sky-200">
          <FormHeader
            title="Створіть нову команду"
            linkText="Повернутись до моїх команд"
            linkHref="/teams"
          />
          <TeamCreateForm/>
        </div>
      </div>
    </div>
  )
}