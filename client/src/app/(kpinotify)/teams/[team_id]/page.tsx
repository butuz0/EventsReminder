"use client";

import {useGetTeamDetailsQuery, useGetTeamEventsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";
import EventsTable from "@/components/events/EventsTable";
import PageTitle from "@/components/shared/PageTitle";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import {clsx} from "clsx";
import TeamInvitationsTable from "@/components/teams/TeamInvitationsTable";
import {Button} from "@/components/ui/button";
import Search from "@/components/shared/Search";
import Link from "next/link";

interface TeamDetails {
  params: {
    team_id: string
  }
}


export default function TeamDetails({params}: TeamDetails) {
  const {data: team, isLoading, isError} = useGetTeamDetailsQuery(params.team_id);
  const {data: events} = useGetTeamEventsQuery(params.team_id);
  const {data: user} = useGetCurrentUserQuery();
  
  if (isLoading) {
    return <LoaderComponent
      size="lg"
      text="Завантаження команди..."
      className="h-3/5"
    />
  }
  
  if (isError || !team) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити Ваші команди. Спробуйте ще раз.
      </div>
    )
  }
  
  const isTeamCreator = user?.id === team?.team.created_by.id;
  
  return (
    <div className="mx-auto max-w-4xl">
      <PageTitle title={team.team.name}/>
      <Tabs defaultValue="events" className="w-full">
        <TabsList className={
          clsx("grid w-full", {
            "grid-cols-3": isTeamCreator,
            "grid-cols-2": !isTeamCreator,
          })}
        >
          <TabsTrigger value="events">
            Події команди
          </TabsTrigger>
          
          <TabsTrigger value="info">
            Про команду
          </TabsTrigger>
          
          {isTeamCreator && (
            <TabsTrigger value="invitations">
              Запрошення у команду
            </TabsTrigger>
          )}
        </TabsList>
        
        <TabsContent value="events">
          <div className="mb-4 flex items-center justify-between gap-4">
            <Search placeholder="Пошук події..."/>
            
            {isTeamCreator && (
              <Button asChild>
                <Link href={`/teams/${params.team_id}/create-event/`}>
                  Додати подію
                </Link>
              </Button>
            )}
          </div>
          <EventsTable
            events={events?.events.results ?? []}
          />
        </TabsContent>
        
        <TabsContent value="info">
          <p>{JSON.stringify(team?.team)}</p>
        </TabsContent>
        
        {isTeamCreator && (
          <TabsContent value="invitations">
            <TeamInvitationsTable teamId={params.team_id}/>
          </TabsContent>
        )}
      </Tabs>
    </div>
  )
}