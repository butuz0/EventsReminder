"use client";

import {useGetAllProfilesQuery} from "@/lib/redux/slices/users/usersApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import ProfileCard from "@/components/profiles/ProfileCard";
import React from "react";

interface ProfilesListProps {
  queryParams?: Record<string, any>;
}

export default function ProfilesList({queryParams = {}}: ProfilesListProps) {
  const {data, isLoading, isError} = useGetAllProfilesQuery(queryParams);
  
  if (isLoading) {
    return (
      <LoaderComponent
        size="lg"
        text="Завантаження користувачів..."
        className="h-3/5"
      />
    );
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити користувачів.
      </div>
    );
  }
  
  const users = data.profiles.results;
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {users.map((profile) => (
        <ProfileCard key={profile.id} profile={profile}/>
      ))}
    </div>
  );
}
