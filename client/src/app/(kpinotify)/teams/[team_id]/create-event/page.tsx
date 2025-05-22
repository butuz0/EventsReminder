"use client";

import EventForm from "@/components/forms/events/EventForm";
import {useGetTeamDetailsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {useRouter} from "next/navigation";
import PageTitle from "@/components/shared/PageTitle";

interface CreateEventPageProps {
  params: {
    team_id: string;
  };
}


export default function CreateTeamEventPage({params}: CreateEventPageProps) {
  const router = useRouter();
  const {data: team, isLoading, isError} = useGetTeamDetailsQuery(params.team_id);
  const {data: user} = useGetCurrentUserQuery();
  
  if (isLoading) {
    return <LoaderComponent
      size="lg"
      className="h-3/5"
    />
  }
  
  if (isError || !team) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити сторінку. Спробуйте ще раз.
      </div>
    )
  }
  
  if (!(user?.id === team?.team.created_by.id)) {
    router.push("/teams");
  }
  
  return (
    <div className="w-full flex flex-col items-center">
      <PageTitle title={team.team.name}/>
      <EventForm teamId={team.team.id}/>
    </div>
  )
}