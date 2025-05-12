"use client"

import {useGetEventDetailsQuery} from "@/lib/redux/slices/events/eventsApiSlice";
import {formatDateTime, dateTimeDistanceToNow} from "@/utils/formatDateTime";
import {Badge} from "@/components/ui/badge";
import PriorityBadge from "@/components/events/PriorityBadge";
import React from "react";
import LoaderComponent from "@/components/shared/Loader";
import {Button} from "@/components/ui/button";
import Link from "next/link";

interface EventDetailProps {
  event_id: string;
}


export default function EventDetailPage({event_id}: EventDetailProps) {
  const {data, isLoading, isError} = useGetEventDetailsQuery(event_id);
  
  if (isLoading) {
    return <LoaderComponent
      size="xl"
      text="Завантаження події..."
      className="h-3/4"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center font-medium text-red-600">
        Не вдалося завантажити подію. Спробуйте ще раз.
      </div>
    )
  }
  
  const {
    title,
    description,
    start_datetime,
    location,
    link,
    image_url,
    priority,
    tags,
    created_by,
    assigned_to,
    is_recurring,
    recurring_event
  } = data.event;
  
  return (
    <div className="mx-auto max-w-4xl rounded-xl bg-gray-100 p-5 shadow-md space-y-6">
      <div className="rounded-xl bg-white p-6 shadow-md space-y-4">
        <h1 className="text-2xl font-bold">{title}</h1>
        {description && <p className="text-gray-800">{description}</p>}
      </div>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Дата та час"
                   value={`${formatDateTime(start_datetime)} - ${dateTimeDistanceToNow(start_datetime)}`}/>
        <InfoBlock
          label="Пріоритет"
          value={
            <PriorityBadge
              priority={priority}
              className="text-lg"
            />
          }
        />
      </div>
      {image_url && (
        <InfoBlock
          label="Зображення"
          value={(
            <div
              className="w-full aspect-[3/2] overflow-hidden rounded-xl border
              border-gray-300 shadow-md bg-white my-4">
              <img
                src={image_url}
                alt={`Зображення події`}
                className="h-full w-full object-cover"
                loading="lazy"
              />
            </div>
          )}
        />
      )}
      
      {tags?.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {tags.map(tag => (
            <Badge
              key={tag}
              variant="secondary"
              className="border border-blue-900 bg-sky-100 p-2 text-blue-900 text-md"
            >
              {tag}
            </Badge>
          ))}
        </div>
      )}
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Місце" value={location || "Не вказано"}/>
        <InfoBlock
          label="Повторювана подія"
          value={
            <div>
              {is_recurring ? "Так" : "Ні"}
            </div>
          }/>
        {link && (
          <InfoBlock
            label="Посилання"
            value={
              <a href={link} target="_blank" className="text-blue-600 underline">
                Відкрити
              </a>
            }
          />
        )}
      </div>
      
      <div className="flex justify-between">
        <Button asChild>
          <Link href={`events/${event_id}/edit`}>
            Змінити
          </Link>
        </Button>
        
        <Button
          asChild
          className="bg-red-600 hover:bg-red-700"
        >
          <Link href={`events/${event_id}/delete`}>
            Видалити
          </Link>
        </Button>
      </div>
    </div>
  )
}


function InfoBlock({label, value}: { label: string; value: React.ReactNode }) {
  return (
    <div className="rounded-xl bg-white p-4 shadow-md">
      <div className="text-sm text-gray-700">{label}</div>
      <div className="text-lg font-medium">{value}</div>
    </div>
  )
}
