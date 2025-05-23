"use client";

import {Profile} from "@/types";
import {UserCircleIcon} from "@heroicons/react/24/solid";
import {UserPlusIcon} from "@heroicons/react/24/outline";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import InviteUserDialog from "@/components/teams/InviteUserDialog";

interface ProfileCardProps {
  profile: Profile;
}


export default function ProfileCard({profile}: ProfileCardProps) {
  const fullName = `${profile.last_name} ${profile.first_name}`;
  const faculty = profile.faculty_abbreviation;
  const department = profile.department_abbreviation;
  const position = profile.position;
  
  return (
    <Card className="relative flex flex-col items-center bg-white
    shadow-md rounded-xl p-4 border border-gray-200">
      <InviteUserDialog
        user={profile}
        className="absolute top-3 right-3"
      />
      
      <CardHeader className="flex items-center justify-center p-0 gap-0">
        {profile.avatar_url ? (
          <img
            src={profile.avatar_url}
            alt={`Avatar of ${fullName}`}
            className="w-20 h-20 rounded-full object-cover border border-gray-300"
          />
        ) : (
          <div className="w-20 h-20 flex items-center justify-center">
            <UserCircleIcon className="w-20 text-gray-500"/>
          </div>
        )}
      </CardHeader>
      <CardContent className="text-center p-0 space-y-1">
        <CardTitle className="text-lg font-semibold">{fullName}</CardTitle>
        <p className="text-sm text-gray-700">{position}</p>
        <p className="text-sm text-gray-500">
          {department} - {faculty}
        </p>
      </CardContent>
    </Card>
  );
}
