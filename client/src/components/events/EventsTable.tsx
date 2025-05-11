"use client"

import Link from "next/link";
import clsx from "clsx";
import {Event} from "@/types";
import PriorityBadge from "@/components/events/PriorityBadge";


interface EventsTableProps {
  events: Event[]
}


export default function EventsTable({events}: EventsTableProps) {
  return (
    <div className="rounded-xl bg-gray-100 p-2 shadow-lg">
      <div className="grid grid-cols-[1fr_2fr_2fr_1fr] rounded-t-xl px-4 py-5 font-semibold">
        <div>Назва</div>
        <div>Опис</div>
        <div>Дата і час</div>
        <div>Пріоритет</div>
      </div>
      
      <div className="divide-y-2 divide-gray-100 text-sm">
        {events.map((event, i) => {
          const isFirst = i === 0;
          const isLast = i === events.length - 1;
          
          const date = new Date(event.start_datetime);
          
          const formattedDate = date.toLocaleString("uk-UA", {
            dateStyle: "medium",
            timeStyle: "short",
          });
          
          return (
            <Link
              key={event.id}
              href={`/events/${event.id}`}
              className={clsx(
                "grid grid-cols-[1fr_2fr_2fr_1fr] bg-white " +
                "px-4 py-5 transition-colors hover:bg-gray-200",
                {
                  "rounded-t-md": isFirst,
                  "rounded-b-md": isLast
                }
              )}
            >
              <div>{event.title}</div>
              <div>{String(event.description).substring(0, 30) + "..."}</div>
              <div>{formattedDate}</div>
              <div>
                <PriorityBadge priority={event.priority}/>
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
