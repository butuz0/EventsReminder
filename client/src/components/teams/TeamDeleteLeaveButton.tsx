"use client";

import DeletionDialog from "@/components/shared/DeletionDialog";
import React from "react";
import {useRouter} from "next/navigation";
import {useDeleteTeamMutation, useLeaveTeamMutation} from "@/lib/redux/slices/teams/teamsApiSlice";
import {toast} from "react-toastify";

interface TeamDeleteLeaveButtonProps {
  teamId: string,
  isTeamCreator: boolean,
}


export default function TeamDeleteLeaveButton({teamId, isTeamCreator = false}: TeamDeleteLeaveButtonProps) {
  const router = useRouter();
  const [deleteTeam] = useDeleteTeamMutation();
  const [leaveTeam] = useLeaveTeamMutation();
  
  const deleteLeaveTeamAction = async () => {
    try {
      if (isTeamCreator) {
        await deleteTeam(teamId).unwrap();
        toast.success("Ви успішно видалили команду")
      } else {
        await leaveTeam(teamId).unwrap();
        toast.success("Ви успішно покинули команду")
      }
      router.push("/teams");
    } catch (error) {
      toast.error("Сталась помилка");
    }
  }
  
  return (
    <DeletionDialog
      buttonText={`${isTeamCreator ? "Видалити" : "Покинути"} команду`}
      confirmButtonText={isTeamCreator ? "Видалити" : "Покинути"}
      onConfirmAction={deleteLeaveTeamAction}
    >
      <p>Ви впевнені що хочете {isTeamCreator ? "видалити" : "покинути"} цю команду?</p>
    </DeletionDialog>
  )
}