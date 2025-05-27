import UpcomingEventsCard from "@/components/events/UpcomingEventsCard";
import UpcomingRemindersCard from "@/components/events/UpcomingNotificationsCard";
import AssignedToMeCard from "@/components/events/AssignedEventsCard";
import PageTitle from "@/components/shared/PageTitle";


export default function Home() {
  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <PageTitle title="Головна сторінка"/>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <UpcomingEventsCard/>
        <UpcomingRemindersCard/>
        <AssignedToMeCard/>
      </div>
    </div>
  );
}
