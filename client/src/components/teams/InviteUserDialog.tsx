"use client";

import {Button} from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {UserPlusIcon} from "@heroicons/react/24/outline";
import React, {useState} from "react";
import {toast} from "react-toastify";
import {Profile} from "@/types";
import {useCreateInvitationMutation} from "@/lib/redux/slices/invitations/invitationsApiSlice";
import {useGetMyTeamsQuery} from "@/lib/redux/slices/teams/teamsApiSlice";
import {useGetCurrentUserQuery} from "@/lib/redux/slices/auth/authApiSlice";
import LoaderComponent from "@/components/shared/Loader";

interface InviteUserDialogProps {
  user: Profile,
  className: string,
}


export default function InviteUserDialog({user, className}: InviteUserDialogProps) {
  const [createInvitation] = useCreateInvitationMutation();
  const {data: teamsData, isLoading, isError} = useGetMyTeamsQuery({});
  const {data: currentUser} = useGetCurrentUserQuery();
  const [open, setOpen] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  
  if (isLoading) {
    return (
      <LoaderComponent
        size="xl"
        text="Завантаження команд..."
        className="h-1/2"
      />
    );
  }
  
  if (isError || !teamsData) {
    return (
      <div className="text-center font-medium text-red-600">
        Не вдалося завантажити Ваші команди. Спробуйте пізніше.
      </div>
    );
  }
  
  const teams = teamsData?.teams.results.filter((team) =>
    team.created_by?.id === currentUser?.id &&
    !team.members?.some((member) => member.id === user.id)
  );
  
  if (teams?.length === 0) {
    return (
      <UserPlusIcon
        className={`w-6 text-gray-500 p-0 ${className}`}
        title="Немає команд, до яких можна запросити користувача."
      />
    )
  }
  
  const onSubmit = async () => {
    if (!selectedTeam) {
      toast.warning("Оберіть команду");
      return;
    }
    
    try {
      await toast.promise(createInvitation({team: selectedTeam, sent_to: user?.id}).unwrap(), {
        pending: "Створюємо запрошення...",
        success: "Запрошення успішно створено!"
      })
    } catch (error) {
      
    }
  }
  
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild className={className}>
        <Button
          asChild
          variant="ghost"
          className="hover:cursor-pointer !p-0 hover:bg-white"
        >
          <UserPlusIcon
            className="w-6 cursor-pointer text-blue-600 hover:text-blue-800"
            title="Запросити до команди"
          />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] border-sky-200">
        <DialogHeader>
          <DialogTitle>
            Запросити користувача
          </DialogTitle>
        </DialogHeader>
        
        <DialogDescription>
          Запросити користувача {user.last_name} {user.first_name} у команду
        </DialogDescription>
        
        <div className="space-y-3 py-2">
          {teams?.map((team) => (
              <label
                key={team.id}
                className="flex items-center gap-2 cursor-pointer"
              >
                <input
                  type="radio"
                  name="team"
                  value={team.id}
                  checked={selectedTeam === team.id}
                  onChange={() => setSelectedTeam(team.id)}
                  className="h-4 w-4 text-sky-600 border-gray-300"
                />
                <span className="text-sm font-medium">{team.name}</span>
              </label>
            )
          )}
        </div>
        
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
            onClick={async () => {
              try {
                await onSubmit();
                setOpen(false);
              } catch (e) {
                toast.error("Сталась помилка");
              }
            }}
          >
            Запросити
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
