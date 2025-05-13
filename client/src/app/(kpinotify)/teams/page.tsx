import PageTitle from "@/components/shared/PageTitle";
import TeamsList from "@/components/teams/TeamsList";


export default function Teams() {
  return (
    <div>
      <PageTitle title="Ваші команди"/>
      <TeamsList/>
    </div>
  );
}
