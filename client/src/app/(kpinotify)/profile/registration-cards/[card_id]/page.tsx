import RegistrationCardDetail from "@/components/registrationCards/RegistrationCardDetail";
import PageTitle from "@/components/shared/PageTitle";

interface RegistrationCardPageProps {
  params: {
    card_id: string;
  }
}


export default async function RegistrationCardPage({params}: RegistrationCardPageProps) {
  const {card_id} = params;
  
  return (
    <div>
      <PageTitle title="Реєстраційна картка АЦСК"/>
      <RegistrationCardDetail cardId={card_id}/>
    </div>
  )
}
