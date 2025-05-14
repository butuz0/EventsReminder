"use client";

import {
  useGetInvitationDetailsQuery,
  useDeleteInvitationMutation,
  useRespondToInvitationMutation
} from "@/lib/redux/slices/invitations/invitationsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import {Button} from "@/components/ui/button";
import {useRouter} from "next/navigation";
import {toast} from "react-toastify";
import InvitationStatusBadge from "@/components/teams/InvitationStatusBadge";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import {formatDateTime} from "@/utils/formatDateTime";
import InfoBlock from "@/components/shared/InfoBlock";
import React from "react";

interface InvitationDetailProps {
  invitationId: string;
}


export default function InvitationDetail({invitationId}: InvitationDetailProps) {
  const {data, isLoading, isError} = useGetInvitationDetailsQuery(invitationId);
  const [respondToInvitation] = useRespondToInvitationMutation();
  const [deleteInvitation] = useDeleteInvitationMutation();
  const {data: user} = useGetCurrentUserQuery();
  const router = useRouter();
  
  if (isLoading) {
    return <LoaderComponent
      size="xl"
      text="Завантаження запрошення..."
      className="h-3/5"
    />
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити запрошення. Спробуйте ще раз.
      </div>
    );
  }
  
  const invitation = data.invitations;
  const isRecipient = user?.id === invitation.sent_to.id;
  const isCreator = user?.id === invitation.created_by.id;
  
  const handleRespond = async (status: "a" | "r") => {
    try {
      await respondToInvitation({invitationId, status}).unwrap();
      toast.success(status === "a" ? "Запрошення прийнято" : "Запрошення відхилено");
      router.push("/teams");
    } catch {
      toast.error("Помилка відповіді на запрошення");
    }
  };
  
  const handleDelete = async () => {
    try {
      await deleteInvitation(invitationId).unwrap();
      toast.success("Запрошення видалено");
      router.push("/teams");
    } catch {
      toast.error("Помилка видалення запрошення");
    }
  };
  
  return (
    <div className="mx-auto max-w-3xl rounded-xl bg-gray-100 p-5 shadow-md space-y-6">
      <div className="rounded-lg bg-white p-6 shadow-md space-y-4">
        <h1 className="text-2xl font-bold">{invitation.team_name}</h1>
        <p className="text-gray-800">{invitation.team_description || "Без опису"}</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <InfoBlock label="Відправник:">
          <p>
            {`${invitation.created_by.last_name} ${invitation.created_by.first_name}`}
          </p>
        </InfoBlock>
        
        <InfoBlock label="Одержувач:">
          <p>
            {`${invitation.sent_to.last_name} ${invitation.sent_to.first_name}`}
          </p>
        </InfoBlock>
        
        <InfoBlock label="Статус:">
          <InvitationStatusBadge status={invitation.status}/>
        </InfoBlock>
        
        <InfoBlock label="Надіслано:">
          <p>
            {formatDateTime(invitation.created_at)}
          </p>
        </InfoBlock>
      </div>
      
      {isRecipient && invitation.status === "p" && (
        <div className="flex justify-between">
          <Button
            className="hover:cursor-pointer"
            variant="destructive"
            onClick={() => handleRespond("r")}
          >
            Відхилити
          </Button>
          <Button
            className="hover:cursor-pointer"
            onClick={() => handleRespond("a")}
          >
            Прийняти
          </Button>
        </div>
      )}
      {isCreator && (
        <div className="flex justify-between">
          <Button
            className="hover:cursor-pointer"
            variant="destructive"
            onClick={handleDelete}
          >
            Видалити запрошення
          </Button>
        </div>
      )}
    </div>
  );
}
