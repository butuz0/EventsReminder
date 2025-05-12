import {Badge} from "@/components/ui/badge";
import {PriorityOptions} from "@/constants";

const priorityColorMap: Record<number, string> = {
  1: "bg-green-100 text-green-700 border-green-700",
  2: "bg-yellow-100 text-yellow-700 border-yellow-700",
  3: "bg-orange-100 text-orange-700 border-orange-700",
  4: "bg-red-100 text-red-700 border-red-700",
}

interface PriorityBadgeProps {
  priority: number,
  className?: string,
}

export default function PriorityBadge({priority, className}: PriorityBadgeProps) {
  const priorityText = PriorityOptions.find(p => p.value === priority)?.label ?? "Невідомо";
  const priorityBadgeStyle = priorityColorMap[priority];
  
  return (
    <Badge className={`${priorityBadgeStyle} ${className}`}>
      {priorityText}
    </Badge>
  )
}