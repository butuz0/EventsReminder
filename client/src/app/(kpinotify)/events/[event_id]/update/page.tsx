"use client";


import PageTitle from "@/components/shared/PageTitle";
import {useGetEventDetailsQuery} from "@/lib/redux/slices/events/eventsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import EventUpdateForm from "@/components/forms/events/EventUpdateForm";

interface PageProps {
  params: {
    event_id: string
  }
}


export default function UpdateEventPage({params}: PageProps) {
  const {data: eventData, isLoading, isError} = useGetEventDetailsQuery(params.event_id);
  
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
  
  return (
    <div className="mx-auto max-w-4xl">
      <PageTitle
        title={eventData.event.title}
      />
      <EventUpdateForm event={eventData.event}/>
    </div>
  )
}