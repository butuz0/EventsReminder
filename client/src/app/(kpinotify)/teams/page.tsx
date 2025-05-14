import PageTitle from "@/components/shared/PageTitle";
import TeamsList from "@/components/teams/TeamsList";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import Search from "@/components/shared/Search";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import InvitationsTable from "@/components/teams/InvitationsTable";


export default function Teams() {
  return (
    <div>
      <PageTitle title="Ваші команди"/>
      <Tabs defaultValue="teams">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="teams">Команди</TabsTrigger>
          <TabsTrigger value="invitations">Запрошення</TabsTrigger>
        </TabsList>
        <TabsContent value="teams">
          <div className="mb-4 flex flex-row gap-4">
            <Search placeholder="Шукати команду"/>
            <Button asChild>
              <Link href="/teams/create">
                Створити команду
              </Link>
            </Button>
          </div>
          <TeamsList/>
        </TabsContent>
        <TabsContent value="invitations">
          <InvitationsTable/>
        </TabsContent>
      </Tabs>
    </div>
  
  );
}
