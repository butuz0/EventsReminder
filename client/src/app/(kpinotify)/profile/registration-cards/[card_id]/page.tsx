import RegistrationCardDetail from "@/components/registrationCards/RegistrationCardDetail";
import PageTitle from "@/components/shared/PageTitle";

interface RegistrationCardPageProps {
  params: {
    card_id: string;
  }
}


export default async function RegistrationCardPage({params}: RegistrationCardPageProps) {
  const {card_id} = await params;
  
  console.log(card_id);
  console.log(card_id);
  console.log(card_id);
  console.log(card_id);
  console.log(card_id);
  
  return (
    <div>
      <PageTitle title="Реєстраційна картка АЦСК"/>
      <RegistrationCardDetail cardId={card_id}/>
    </div>
  )
}
