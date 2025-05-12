import EventDetailPage from "@/components/events/EventDetailPage";
import PageTitle from "@/components/shared/PageTitle";

interface PageProps {
  params: { event_id: string }
}


export default async function EventDetail({params}: PageProps) {
  const {event_id} = await params;
  
  return (
    <div className="h-full">
      <PageTitle
        title="Деталі події"
      />
      
      <EventDetailPage event_id={event_id}/>
    </div>
  )
}
