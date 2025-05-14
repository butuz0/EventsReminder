import InvitationDetail from "@/components/teams/InvitationDetail";
import PageTitle from "@/components/shared/PageTitle";

interface InvitationDetailPageProps {
  params: {
    invitation_id: string
  }
}


export default function InvitationDetailPage({params}: InvitationDetailPageProps) {
  const invitation_id = params.invitation_id;
  
  return (
    <div>
      <PageTitle title="Запрошення у команду"/>
      <InvitationDetail invitationId={invitation_id}/>
    </div>
  )
}