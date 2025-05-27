"use client";

import {useGetMyEventsQuery} from "@/lib/redux/slices/events/eventsApiSlice";
import {formatDateTime, dateTimeDistanceToNow} from "@/utils/formatDateTime";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import InfoBlock from "@/components/shared/InfoBlock";


export default function AssignedToMeCard() {
  const {data, isLoading} = useGetMyEventsQuery({ordering: "-created_at"});
  const {data: currentUser} = useGetCurrentUserQuery();
  
  const assigned = (data?.events.results ?? [])
    .filter((event) => event.assigned_to?.some(
      (user) => user.id === currentUser?.id)
    )
    .slice(0, 3);
  
  return (
    <InfoBlock label="Останні призначені події">
      {isLoading ? (
        <p>Завантаження...</p>
      ) : assigned.length === 0 ? (
        <p>Немає призначених подій</p>
      ) : (
        assigned.map((event) => (
          <div key={event.id}>
            <strong>{event.title}</strong><br/>
            Призначено {formatDateTime(event.created_at)}
          </div>
        ))
      )}
    </InfoBlock>
  )
}
