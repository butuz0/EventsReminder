"use client";

import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {formatDateTime} from "@/utils/formatDateTime";
import Link from "next/link";
import clsx from "clsx";
import InvitationStatusBadge from "@/components/teams/InvitationStatusBadge";
import {useGetTeamInvitationsQuery} from "@/lib/redux/slices/invitations/invitationsApiSlice";
import {Button} from "@/components/ui/button";

interface TeamInvitationsTableProps {
  teamId: string;
}


export default function TeamInvitationsTable({teamId}: TeamInvitationsTableProps,) {
  const {data, isLoading, isError} = useGetTeamInvitationsQuery(teamId);
  
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
        Не вдалося завантажити запрошення у команду. Спробуйте ще раз.
      </div>
    )
  }
  
  const invitations = data?.invitations.results;
  
  if (invitations.length === 0) {
    return (
      <div className="text-center space-y-2">
        <div className="text-gray-600 font-medium">
          Запрошень до цієї команди не знайдено
        </div>
        <Button asChild>
          <Link href={"/teams/invitations/create/"}>
            Створити запрошення
          </Link>
        </Button>
      </div>
    );
  }
  
  return (
    <div>
      <div className="flex justify-between items-end mb-2">
        <p>Запрошення у команду</p>
        <Button asChild>
          <Link href={"/teams/invitations/create/"}>
            Створити запрошення
          </Link>
        </Button>
      </div>
      
      <div className="rounded-xl bg-gray-100 p-2 shadow-lg">
        <div className="grid grid-cols-[3fr_3fr_1fr] rounded-t-xl px-4 py-5 font-semibold">
          <div>Ім'я</div>
          <div>Дата і час</div>
          <div>Статус</div>
        </div>
        
        <div className="divide-y-2 divide-gray-100 text-sm">
          {invitations.map((invitation, i) => {
            const isFirst = i === 0;
            const isLast = i === invitations.length - 1;
            
            return (
              <Link
                key={invitation.id}
                href={`/teams/invitations/${invitation.id}`}
                className={clsx(
                  "grid grid-cols-[3fr_3fr_1fr] bg-white " +
                  "px-4 py-5 transition-colors hover:bg-gray-200",
                  {
                    "rounded-t-md": isFirst,
                    "rounded-b-md": isLast
                  }
                )}
              >
                <div>{invitation.sent_to.last_name} {invitation.sent_to.first_name}</div>
                <div>{formatDateTime(invitation.created_at)}</div>
                <div>
                  <InvitationStatusBadge status={invitation.status}/>
                </div>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  );
}