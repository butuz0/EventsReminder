"use client";

import DeletionDialog from "@/components/shared/DeletionDialog";
import React from "react";
import {useRouter} from "next/navigation";
import {toast} from "react-toastify";
import {useDeleteEventMutation, useLeaveEventMutation} from "@/lib/redux/slices/events/eventsApiSlice";

interface EventDeleteLeaveButtonProps {
  eventId: string,
  isTeamCreator: boolean,
}


export default function EventDeleteLeaveButton({eventId, isTeamCreator = false}: EventDeleteLeaveButtonProps) {
  const router = useRouter();
  const [deleteEvent] = useDeleteEventMutation();
  const [leaveEvent] = useLeaveEventMutation();
  
  const deleteLeaveTeamAction = async () => {
    try {
      if (isTeamCreator) {
        await deleteEvent(eventId).unwrap();
        toast.success("Ви успішно видалили подію")
      } else {
        await leaveEvent(eventId).unwrap();
        toast.success("Ви успішно відмовились від події")
      }
      router.push("/events");
    } catch (error) {
      toast.error("Сталась помилка");
    }
  }
  
  return (
    <DeletionDialog
      buttonText={isTeamCreator ? "Видалити подію" : "Відмовитись від події"}
      confirmButtonText={isTeamCreator ? "Видалити" : "Відмовитись"}
      onConfirmAction={deleteLeaveTeamAction}
    >
      <p>
        Ви впевнені що хочете {isTeamCreator
        ? "видалити цю подію?"
        : "відмовитись від цієї події?"}
      </p>
    </DeletionDialog>
  )
}