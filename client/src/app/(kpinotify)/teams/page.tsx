import PageTitle from "@/components/shared/PageTitle";
import TeamsList from "@/components/teams/TeamsList";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import Search from "@/components/shared/Search";


export default function Teams() {
  return (
    <div>
      <PageTitle title="Ваші команди"/>
      <div className="mb-4 flex flex-row gap-4">
        <Search placeholder="Шукати команду"/>
        <Button asChild>
          <Link href="/teams/create">
            Створити команду
          </Link>
        </Button>
      </div>
      <TeamsList/>
    </div>
  );
}
