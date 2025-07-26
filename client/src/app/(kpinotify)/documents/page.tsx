import {Button} from "@/components/ui/button";
import Link from "next/link";
import RegistrationCardsTable from "@/components/registrationCards/RegistrationCardsTable";
import PageTitle from "@/components/shared/PageTitle";


export default function DocumentsPage() {
  return (
    <div>
      <PageTitle title="Ваші документи"/>
      <Button asChild className="mb-2">
        <Link href={"/documents/registration-cards/create"}>
          Додати картку
        </Link>
      </Button>
      <RegistrationCardsTable/>
    </div>
  )
}
