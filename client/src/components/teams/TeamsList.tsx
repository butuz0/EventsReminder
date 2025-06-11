"use client";

import {useGetMyTeamsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {TeamCard} from "@/components/teams/TeamCard";

interface TeamsListProps {
  teamParams?: Record<string, any>;
}


export default function TeamsList({teamParams = {}}: TeamsListProps) {
  const {data, isLoading, isError} = useGetMyTeamsQuery(teamParams);
  
  if (isLoading) {
    return <LoaderComponent
      size="lg"
      text="Завантаження ваших команд..."
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
  
  const teams = data?.teams.results;
  
  if (teams.length === 0) {
    return (
      <div className="text-center font-medium">
        Ви не є членом жодної команди.
      </div>
    )
  }
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {teams.map((team) => (
        <TeamCard key={team.id} team={team}/>
      ))}
    </div>
  );
}