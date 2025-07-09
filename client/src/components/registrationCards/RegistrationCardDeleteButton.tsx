"use client";

import DeletionDialog from "@/components/shared/DeletionDialog";
import React from "react";
import {useRouter} from "next/navigation";
import {toast} from "react-toastify";
import {useDeleteRegistrationCardMutation} from "@/lib/redux/slices/registrationCards/registrationCardsApiSlice";

interface RegistrationCardDeleteButtonProps {
  registrationCardId: string,
}


export default function RegistrationCardDeleteButton({registrationCardId}: RegistrationCardDeleteButtonProps) {
  const router = useRouter();
  const [deleteRegistrationCard] = useDeleteRegistrationCardMutation();
  
  const deleteRegistrationCardAction = async () => {
    try {
      await deleteRegistrationCard(registrationCardId).unwrap();
      toast.success("Ви успішно видалили картку АЦСК")
      router.push("/profile");
    } catch {
      toast.error("Сталась помилка");
    }
  }
  
  return (
    <DeletionDialog
      buttonText="Видалити картку"
      confirmButtonText="Видалити"
      onConfirmAction={deleteRegistrationCardAction}
    >
      <p>
        Ви впевнені що хочете видалити цю картку?
      </p>
    </DeletionDialog>
  )
}