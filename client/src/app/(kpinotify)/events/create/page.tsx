import EventCreateForm from "@/components/forms/events/EventCreateForm";
import PageTitle from "@/components/shared/PageTitle";


export default function CreateEventPage() {
  return (
    <div className="w-full flex flex-col items-center">
      <PageTitle title="Додайте подію"/>
      <EventCreateForm/>
    </div>
  )
}