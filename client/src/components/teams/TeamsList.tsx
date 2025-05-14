"use client";

import {useGetMyTeamsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {TeamCard} from "@/components/teams/TeamCard";


export default function TeamsList() {
  const {data, isLoading, isError} = useGetMyTeamsQuery();
  
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
  
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {teams.map((team) => (
        <TeamCard key={team.id} team={team}/>
      ))}
    </div>
  );
}