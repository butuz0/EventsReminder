import {Badge} from "@/components/ui/badge";
import {InvitationStatusOptions} from "@/constants";

const statusColorMap: Record<string, string> = {
  "p": "bg-blue-100 text-blue-700 border-blue-700",
  "a": "bg-green-100 text-green-700 border-green-700",
  "r": "bg-orange-100 text-orange-700 border-orange-700",
}

interface PriorityBadgeProps {
  status: string,
  className?: string,
}


export default function InvitationStatusBadge({status, className}: PriorityBadgeProps) {
  const statusText = InvitationStatusOptions.find(s =>
    s.value === status)?.label ?? "Невідомо";
  const statusBadgeStyle = statusColorMap[status];
  
  return (
    <Badge className={`${statusBadgeStyle} ${className}`}>
      {statusText}
    </Badge>
  )
}