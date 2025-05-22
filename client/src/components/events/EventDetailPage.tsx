"use client"

import {useGetEventDetailsQuery} from "@/lib/redux/slices/events/eventsApiSlice";
import {formatDateTime, dateTimeDistanceToNow} from "@/utils/formatDateTime";
import {Badge} from "@/components/ui/badge";
import PriorityBadge from "@/components/events/PriorityBadge";
import React from "react";
import LoaderComponent from "@/components/shared/Loader";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import InfoBlock from "@/components/shared/InfoBlock";
import NotificationsList from "@/components/events/NotificationsList";
import getGoogleCalendarLink from "@/utils/getGoogleCalendarLink";
import TeamMembersTable from "@/components/teams/TeamMembersTable";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import EventDeleteLeaveButton from "@/components/events/EventDeleteLeaveButton";

interface EventDetailProps {
  event_id: string;
}


export default function EventDetailPage({event_id}: EventDetailProps) {
  const {data: eventData, isLoading, isError} = useGetEventDetailsQuery(event_id);
  const {data: user} = useGetCurrentUserQuery();
  
  if (isLoading) {
    return <LoaderComponent
      size="xl"
      text="Завантаження події..."
      className="h-3/4"
    />
  }
  
  if (isError || !eventData) {
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
    team,
    assigned_to,
    is_recurring,
    recurring_event
  } = eventData.event;
  
  const isCreator = user?.id === created_by.id;
  
  return (
    <div className="mx-auto max-w-4xl rounded-xl border border-gray-200 bg-gray-100 p-5 shadow-md space-y-6">
      <div className="rounded-xl bg-white p-6 shadow-md space-y-4">
        <h1 className="text-2xl font-bold">{title}</h1>
        {description && <p className="text-gray-800">{description}</p>}
      </div>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Дата та час">
          <p>
            {`${formatDateTime(start_datetime)} - ${dateTimeDistanceToNow(start_datetime)}`}
          </p>
        </InfoBlock>
        
        <InfoBlock label="Пріоритет">
          <PriorityBadge
            priority={priority}
            className="text-lg"
          />
        </InfoBlock>
      </div>
      
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
      
      {team && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <InfoBlock label="Команда">
            <p>{team.name}</p>
          </InfoBlock>
          <InfoBlock label="Створено">
            <p>{created_by.last_name} {created_by.first_name}</p>
          </InfoBlock>
        </div>
      )}
      
      {assigned_to.length > 0 && (
        <InfoBlock label="Призначено для">
          <TeamMembersTable
            members={assigned_to}
            showAction={false}
          />
        </InfoBlock>
      )}
      
      {image_url && (
        <InfoBlock label="Зображення">
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
        </InfoBlock>
      )}
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Місце">
          <p>{location || "Не вказано"}</p>
        </InfoBlock>
        
        <InfoBlock label="Повторювана подія">
          <p>{is_recurring ? "Так" : "Ні"}</p>
        </InfoBlock>
        {link && (
          <InfoBlock label="Посилання">
            <a href={link}
               target="_blank"
               className="text-blue-600 underline"
            >
              Відкрити
            </a>
          </InfoBlock>
        )}
      </div>
      
      <NotificationsList eventId={event_id}/>
      
      <div className="flex justify-between">
        <EventDeleteLeaveButton
          eventId={event_id}
          isTeamCreator={isCreator}
        />
        
        <Button asChild>
          <Link href={getGoogleCalendarLink(eventData.event)} target="_blank">
            Додати до Google Calendar
          </Link>
        </Button>
        
        {isCreator && (
          <Button asChild>
            <Link href={`/events/${event_id}/update`}>
              Змінити
            </Link>
          </Button>
        )}
      
      </div>
    </div>
  )
}
