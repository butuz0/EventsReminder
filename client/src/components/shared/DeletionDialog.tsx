"use client";

import {Button} from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription
} from "@/components/ui/dialog";
import React, {useState} from "react";
import {toast} from "react-toastify";

interface ConfirmDeletionDialogProps {
  buttonText: string,
  confirmButtonText: string,
  onConfirmAction: () => void,
  description?: string,
  children: React.ReactNode,
}


export default function DeletionDialog(
  {
    buttonText,
    confirmButtonText,
    onConfirmAction,
    description,
    children
  }: ConfirmDeletionDialogProps) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
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
          {description && (
            <DialogDescription>
              {description}
            </DialogDescription>
          )}
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
            disabled={isLoading}
            onClick={async () => {
              try {
                setIsLoading(true);
                onConfirmAction();
                setOpen(false);
              } catch (e) {
                toast.error("Сталась помилка");
              } finally {
                setIsLoading(false);
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
