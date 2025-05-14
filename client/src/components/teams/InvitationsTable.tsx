"use client";

import {useGetMyInvitationsQuery} from "@/lib/redux/slices/invitations/invitationsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {formatDateTime} from "@/utils/formatDateTime";
import Link from "next/link";
import clsx from "clsx";
import InvitationStatusBadge from "@/components/teams/InvitationStatusBadge";


export default function InvitationsTable() {
  const {data, isLoading, isError} = useGetMyInvitationsQuery();
  
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
        Не вдалося завантажити Ваші запрошення. Спробуйте ще раз.
      </div>
    )
  }
  
  const invitations = data?.invitations.results;
  
  if (!(invitations.length > 0)) {
    return (
      <div className="text-center font-medium">
        У Вас немає запрошень.
      </div>
    )
  }
  
  return (
    <div className="rounded-xl bg-gray-100 p-2 shadow-lg">
      <div className="grid grid-cols-[2fr_2fr_2fr_1fr] rounded-t-xl px-4 py-5 font-semibold">
        <div>Команда</div>
        <div>Лідер команди</div>
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
                "grid grid-cols-[2fr_2fr_2fr_1fr] bg-white " +
                "px-4 py-5 transition-colors hover:bg-gray-200",
                {
                  "rounded-t-md": isFirst,
                  "rounded-b-md": isLast
                }
              )}
            >
              <div>{invitation.team_name}</div>
              <div>{invitation.created_by.last_name} {invitation.created_by.first_name}</div>
              <div>{formatDateTime(invitation.created_at)}</div>
              <div>
                <InvitationStatusBadge status={invitation.status}/>
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}