"use client"

import {useGetMyEventsQuery} from "@/lib/redux/slices/events/eventsApiSlice"
import EventsTable from "@/components/events/EventsTable";
import PageTitle from "@/components/shared/PageTitle";
import LoaderComponent from "@/components/shared/Loader";
import React, {useMemo, Suspense} from "react";
import Link from "next/link";
import {Button} from "@/components/ui/button";
import Search from "@/components/shared/Search";
import {useSearchParams} from "next/navigation";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";


function EventsPageContent() {
  const searchParams = useSearchParams();
  const params = useMemo(() => ({
    search: searchParams.get("search") || undefined,
    ordering: searchParams.get("ordering") || undefined,
    page: Number(searchParams.get("page") || 1),
  }), [searchParams]);
  
  const {data, isLoading, isError} = useGetMyEventsQuery(params);
  const {data: currentUser} = useGetCurrentUserQuery();
  
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
  
  const events = data?.events.results;
  const now = new Date();
  
  const upcomingEvents = events.filter(event =>
    new Date(event.start_datetime) > now && event.created_by.id === currentUser?.id
  );
  
  const assignedEvents = events.filter(event =>
    new Date(event.start_datetime) > now &&
    event.assigned_to.some(user => user.id === currentUser?.id)
  );
  
  const pastEvents = events.filter(event =>
    new Date(event.start_datetime) < now
  );
  
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
      
      <Tabs defaultValue="upcoming" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upcoming">
            Майбутні
          </TabsTrigger>
          <TabsTrigger value="assigned">
            Призначені
          </TabsTrigger>
          <TabsTrigger value="past">
            Минулі
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="upcoming">
          <EventsTable events={upcomingEvents}/>
        </TabsContent>
        
        <TabsContent value="assigned">
          <EventsTable events={assignedEvents}/>
        </TabsContent>
        
        <TabsContent value="past">
          <EventsTable events={pastEvents}/>
        </TabsContent>
      </Tabs>
    </div>
  )
}


export default function EventsPage() {
  return (
    <Suspense
      fallback={
        <LoaderComponent
          size="lg"
          text="Завантаження подій..."
        />
      }
    >
      <EventsPageContent/>
    </Suspense>
  );
}