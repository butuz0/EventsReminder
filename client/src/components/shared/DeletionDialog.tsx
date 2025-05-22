"use client";

import {Button} from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import React, {useState} from "react";
import {toast} from "react-toastify";

interface ConfirmDeletionDialogProps {
  buttonText: string,
  confirmButtonText: string,
  onConfirmAction: () => void,
  children: React.ReactNode,
}


export default function DeletionDialog(
  {
    buttonText,
    confirmButtonText,
    onConfirmAction,
    children
  }: ConfirmDeletionDialogProps) {
  const [open, setOpen] = useState(false);
  
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="destructive"
          className="hover:cursor-pointer"
        >
          {buttonText}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {buttonText}
          </DialogTitle>
        </DialogHeader>
        
        {children}
        
        <DialogFooter className="flex sm:justify-between">
          <Button
            variant="outline"
            className="hover:cursor-pointer"
            onClick={() => setOpen(false)}
          >
            Скасувати
          </Button>
          
          <Button
            type="submit"
            className="hover:cursor-pointer"
            variant="destructive"
            onClick={async () => {
              try {
                onConfirmAction();
                setOpen(false);
              } catch (e) {
                toast.error("Сталась помилка");
              }
            }}
          >
            {confirmButtonText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
