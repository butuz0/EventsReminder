import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {Team} from "@/types";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import {formatDate} from "@/utils/formatDateTime";

interface TeamCardProps {
  team: Team;
}


export function TeamCard({team}: TeamCardProps) {
  const description = team.description?.trim() || "Без опису";
  
  return (
    <Card
      className="flex flex-col overflow-hidden
      rounded-xl border border-gray-200 p-2
      bg-gray-100 shadow-sm min-h-[100px]"
    >
      <CardHeader className="m-0 px-2">
        <div className="flex flex-col items-start justify-between space-y-1">
          <CardTitle className="text-lg font-semibold">
            {team.name}
          </CardTitle>
          <CardDescription className="text-sm text-gray-700">
            Створено: {`${team.created_by.last_name} ${team.created_by.first_name}`} <br/>
            {formatDate(team.created_at)}
          
          </CardDescription>
        </div>
      </CardHeader>
      
      <div className="flex flex-1 flex-col justify-between
      bg-white rounded-md p-1 border-gray-200 shadow-sm">
        <CardContent className="text-sm p-2">
          <p className="mb-2">
            {description.length > 80 ? description.slice(0, 77) + "..." : description}
          </p>
          <p>
            Учасників: <strong>{team.members.length}</strong>
          </p>
        </CardContent>
        
        <CardFooter className="flex items-center justify-between
        border-gray-200 m-0 p-2">
          <Button asChild>
            <Link href={`/teams/${team.id}`}>
              Перейти
            </Link>
          </Button>
        </CardFooter>
      </div>
    </Card>
  );
}
