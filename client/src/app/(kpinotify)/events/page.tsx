"use client"

import {useGetMyEventsQuery} from "@/lib/redux/slices/events/eventsApiSlice"
import EventsTable from "@/components/events/EventsTable";
import PageTitle from "@/components/shared/PageTitle";
import LoaderComponent from "@/components/shared/Loader";
import React, {useMemo} from "react";
import Link from "next/link";
import {Button} from "@/components/ui/button";
import Search from "@/components/shared/Search";
import {useSearchParams} from "next/navigation";


export default function EventsPage() {
  const searchParams = useSearchParams();
  const params = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    ordering: searchParams.get("ordering") || undefined,
    page: Number(searchParams.get("page") || 1),
  }), [searchParams]);
  
  const {data, isLoading, isError} = useGetMyEventsQuery(params);
  
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
      
      <div className="mb-4 flex items-center justify-between gap-4">
        <Search placeholder="Пошук події..."/>
        
        <Button asChild>
          <Link href={"/events/create"}>
            Додати подію
          </Link>
        </Button>
      </div>
      
      <EventsTable
        events={data?.events.results ?? []}
      />
    </div>
  )
}
