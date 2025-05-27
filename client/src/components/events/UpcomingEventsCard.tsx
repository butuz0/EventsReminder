"use client";

import {useGetMyEventsQuery} from "@/lib/redux/slices/events/eventsApiSlice";
import {dateTimeDistanceToNow} from "@/utils/formatDateTime";
import Link from "next/link";
import InfoBlock from "@/components/shared/InfoBlock";


export default function UpcomingEventsCard() {
  const now = new Date().setMilliseconds(0);
  const fromDate = new Date(now).toISOString();
  const {data, isLoading} = useGetMyEventsQuery({from_date: fromDate});
  
  const events = data?.events.results.slice(0, 3) ?? [];
  
  return (
    <InfoBlock label="Найближчі події">
      {isLoading ? (
        <p>Завантаження...</p>
      ) : events.length === 0 ? (
        <p>Немає майбутніх подій</p>
      ) : (
        events.map((event) => (
          <div key={event.id}>
            <strong>{dateTimeDistanceToNow(event.start_datetime)}:</strong> {event.title}
          </div>
        ))
      )}
      <Link
        href="/events"
        className="block text-sky-600 hover:underline mt-2"
      >
        Переглянути всі
      </Link>
    </InfoBlock>
  );
}
