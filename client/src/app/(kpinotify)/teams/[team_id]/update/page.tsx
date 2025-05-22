import FormHeader from "@/components/forms/FormHeader";
import TeamUpdateForm from "@/components/forms/teams/TeamUpdateForm";

interface UpdateTeamPageProps {
  params: {
    team_id: string;
  };
}


export default function UpdateTeamPage({params}: UpdateTeamPageProps) {
  return (
    <div className="mx-auto max-w-3xl bg-white rounded-xl
        shadow-md p-4 border border-sky-200">
      <FormHeader
        title="Оновіть команду"
        linkText="Повернутись до команди"
        linkHref={`/teams/${params.team_id}`}
      />
      <TeamUpdateForm teamId={params.team_id}/>
    </div>
  )
}