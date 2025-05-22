import {Team} from "@/types";
import React from "react";
import InfoBlock from "@/components/shared/InfoBlock";
import {formatDate} from "@/utils/formatDateTime";
import TeamMembersTable from "@/components/teams/TeamMembersTable";
import {Button} from "../ui/button";
import TeamDeleteLeaveButton from "@/components/teams/TeamDeleteLeaveButton";
import Link from "next/link";

interface TeamDetailPageProps {
  team: Team
  isTeamCreator: boolean
}


export default function TeamDetail({team, isTeamCreator = false}: TeamDetailPageProps) {
  return (
    <div className="mx-auto max-w-4xl rounded-xl border
    border-gray-200 bg-gray-100 p-5 shadow-md space-y-6">
      <div className="rounded-xl bg-white p-6 shadow-md space-y-4">
        <h1 className="text-2xl font-bold">
          {team.name}
        </h1>
        {team.description &&
            <p className="text-gray-800">
              {team.description}
            </p>
        }
      </div>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Лідер">
          <p>{team.created_by.last_name} {team.created_by.first_name}</p>
        </InfoBlock>
        <InfoBlock label="Створено">
          <p>{formatDate(team.created_at)}</p>
        </InfoBlock>
      </div>
      
      <InfoBlock label="Учасники">
        {team.members.length > 0 ? (
          <TeamMembersTable
            teamId={team.id}
            members={team.members}
            showAction={isTeamCreator}
          />
        ) : (
          <p>
            Немає учасників
          </p>
        )}
      </InfoBlock>
      
      <div className="w-full flex justify-between">
        <TeamDeleteLeaveButton
          teamId={team.id}
          isTeamCreator={isTeamCreator}
        />
        {isTeamCreator && (
          <Button
            asChild
            className="hover:cursor-pointer"
          >
            <Link href={`/teams/${team.id}/update`}>
              Змінити
            </Link>
          </Button>
        )}
      </div>
    </div>
  )
}