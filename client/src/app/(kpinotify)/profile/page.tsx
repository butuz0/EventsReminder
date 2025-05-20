import ProfileDetails from "@/components/profiles/ProfileDetails";
import {Tabs, TabsList, TabsTrigger, TabsContent} from "@/components/ui/tabs";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import RegistrationCardsTable from "@/components/registrationCards/RegistrationCardsTable";


export default function Profile() {
  return (
    <Tabs defaultValue="profile" className="mx-auto max-w-4xl">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="profile">
          Мій профіль
        </TabsTrigger>
        <TabsTrigger value="cards">
          Картки АЦСК
        </TabsTrigger>
      </TabsList>
      <TabsContent value="profile">
        <ProfileDetails/>
      </TabsContent>
      <TabsContent value="cards">
        <Button asChild className="mb-2">
          <Link href={"/profile/registration-cards/create"}>
            Додати
          </Link>
        </Button>
        <RegistrationCardsTable/>
      </TabsContent>
    </Tabs>
  )
}
