"use client";

import {useGetTeamDetailsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";

interface TeamDetails {
  params: {
    team_id: string
  }
}


export default function TeamDetails({params}: TeamDetails) {
  const {data, isLoading, isError} = useGetTeamDetailsQuery(params.team_id);
  
  if (isLoading) {
    return <LoaderComponent
      size="lg"
      text="Завантаження команди..."
      className="h-3/5"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити Ваші команди. Спробуйте ще раз.
      </div>
    )
  }
  
  return (
    <div>
      {JSON.stringify(data?.team)}
    </div>
  )
}