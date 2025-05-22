"use client"

import Link from "next/link";
import clsx from "clsx";
import {Event} from "@/types";
import PriorityBadge from "@/components/events/PriorityBadge";
import {formatDateTime} from "@/utils/formatDateTime";
import {useSearchParams, usePathname, useRouter} from "next/navigation";
import {ChevronDownIcon, ChevronUpIcon} from "@heroicons/react/24/solid";
import {Badge} from "@/components/ui/badge";

interface EventsTableProps {
  events: Event[]
}


export default function EventsTable({events}: EventsTableProps) {
  if (events.length === 0) {
    return (
      <div className="text-center text-gray-600 font-medium">
        Подій не знайдено
      </div>
    )
  }
  
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();
  
  const ordering = searchParams.get("ordering") || "";
  
  const toggleOrdering = (field: string) => {
    const newParams = new URLSearchParams(searchParams.toString());
    const current = ordering === field ? `-${field}` : field;
    
    newParams.set("ordering", current);
    router.push(`${pathname}?${newParams.toString()}`);
  };
  
  const orderingIndicator = (field: string) => {
    if (ordering === field) return <ChevronDownIcon className="ml-1 inline-block w-4"/>;
    if (ordering === `-${field}`) return <ChevronUpIcon className="ml-1 inline-block w-4"/>;
    return null;
  };
  
  return (
    <div className="rounded-xl border border-gray-200 bg-gray-100 p-2 shadow-lg">
      <div className="grid rounded-t-xl px-4 py-5 font-semibold grid-cols-[2fr_4fr_2fr_1fr]">
        <div>
          <button
            onClick={() => toggleOrdering("title")}
            className="text-left hover:cursor-pointer"
          >
            Назва {orderingIndicator("title")}
          </button>
        </div>
        
        <div>Опис</div>
        <div>
          <button
            onClick={() => toggleOrdering("start_datetime")}
            className="text-left hover:cursor-pointer"
          >
            Дата і час {orderingIndicator("start_datetime")}
          </button>
        </div>
        
        <div>
          <button
            onClick={() => toggleOrdering("priority")}
            className="text-left hover:cursor-pointer"
          >
            Пріоритет {orderingIndicator("priority")}
          </button>
        </div>
      </div>
      
      <div className="divide-y-2 divide-gray-100 text-sm">
        {events.map((event, i) => {
          const isFirst = i === 0;
          const isLast = i === events.length - 1;
          
          return (
            <Link
              key={event.id}
              href={`/events/${event.id}`}
              className={clsx(
                "grid grid-cols-[2fr_4fr_2fr_1fr] bg-white " +
                "px-4 py-5 transition-colors hover:bg-gray-200",
                {
                  "rounded-t-md": isFirst,
                  "rounded-b-md": isLast
                }
              )}
            >
              <div className="font-semibold">
                {event.title}
              </div>
              <div className="space-x-1 flex items-center">
                {event.tags.slice(0, 2).map((tag) => (
                  <Badge
                    key={tag}
                    variant="secondary"
                    className="border border-blue-900 bg-sky-100 text-blue-900"
                  >
                    {tag}
                  </Badge>
                ))}
                {event.tags.length > 2 && (
                  <p className="text-gray-500 text-xs">
                    +{event.tags.length - 2}
                  </p>
                )}
                <p>
                  {String(event.description).substring(0, 30) + "..."}
                </p>
              </div>
              <div>{formatDateTime(event.start_datetime)}</div>
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
