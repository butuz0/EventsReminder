"use client";

import {Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogTrigger} from "@/components/ui/dialog";
import {UserMinusIcon} from "@heroicons/react/24/outline";
import {Button} from "@/components/ui/button";
import {useState} from "react";
import {toast} from "react-toastify";
import {useRemoveMemberMutation} from "@/lib/redux/slices/teams/teamsApiSlice";

interface RemoveMemberButtonProps {
  teamId: string;
  memberId: string;
  memberName: string;
}


export default function RemoveTeamMemberButton({teamId, memberId, memberName}: RemoveMemberButtonProps) {
  const [removeMember] = useRemoveMemberMutation();
  
  const [open, setOpen] = useState(false);
  
  const handleConfirm = async () => {
    try {
      await removeMember({teamId, memberId}).unwrap();
      toast.success(`Користувача ${memberName} видалено із команди.`);
      setOpen(false);
    } catch {
      toast.error("Не вдалося видалити користувача.");
    }
  };
  
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          asChild
          className="text-red-600 hover:text-red-800
          hover:cursor-pointer hover:bg-white !p-0"
        >
          <UserMinusIcon className="w-5"/>
        </Button>
      </DialogTrigger>
      
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Вигнати {memberName}?</DialogTitle>
        </DialogHeader>
        
        <p>
          Ви дійсно хочете видалити {memberName} з команди?
        </p>
        
        <DialogFooter className="flex sm:justify-between">
          <Button
            variant="outline"
            className="hover:cursor-pointer"
            onClick={() => setOpen(false)}
          >
            Скасувати
          </Button>
          <Button
            variant="destructive"
            className="hover:cursor-pointer"
            onClick={handleConfirm}
          >
            Вигнати
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
