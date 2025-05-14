import PageTitle from "@/components/shared/PageTitle";
import FacultiesTable from "@/components/units/FacultiesTable";
import {Tabs, TabsList, TabsTrigger, TabsContent} from "@/components/ui/tabs";
import ProfilesList from "@/components/profiles/ProfilesList";


export default function UniversityPage() {
  return (
    <div>
      <PageTitle title="Університет"/>
      <Tabs defaultValue="university">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="university">
            Університет
          </TabsTrigger>
          <TabsTrigger value="users">
            Користувачі
          </TabsTrigger>
        </TabsList>
        <TabsContent value="university">
          <FacultiesTable/>
        </TabsContent>
        <TabsContent value="users">
          <ProfilesList/>
        </TabsContent>
      </Tabs>
    </div>
  
  );
}