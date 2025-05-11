"use client"

import {useGetMyEventsQuery} from "@/lib/redux/slices/events/eventsApiSlice"
import EventsTable from "@/components/events/EventsTable";
import PageTitle from "@/components/shared/PageTitle";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";


export default function EventsPage() {
  const {data, isLoading, isError} = useGetMyEventsQuery();
  
  if (isLoading) {
    return <LoaderComponent
      size="lg"
      text="Завантаження ваших подій..."
      className="h-3/5"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити події. Спробуйте ще раз.
      </div>
    )
  }
  
  return (
    <div>
      <PageTitle title="Ваші події"/>
      <div className="container mx-auto">
        <EventsTable
          events={data?.events.results ?? []}
        />
      </div>
    </div>
  )
}
