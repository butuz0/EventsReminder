import {User} from "@/types";
import RemoveTeamMemberButton from "@/components/teams/RemoveTeamMemberButton";

interface TeamMembersTableProps {
  teamId?: string;
  members: User[];
  showAction: boolean;
}


export default function TeamMembersTable({teamId, members, showAction}: TeamMembersTableProps) {
  return (
    <div className="mt-2 rounded-lg border border-gray-200">
      <div
        className="grid grid-cols-[1fr_1fr_1fr_auto] px-3 py-2 font-semibold
        text-sm text-gray-800 bg-gray-50 rounded-t-xl border-b border-gray-200">
        <p>Імʼя</p>
        <p>Посада</p>
        <p>Кафедра</p>
        {showAction && <p className="text-right">Дії</p>}
      </div>
      
      {members.map((user, index) => (
        <div
          key={user.id}
          className={`grid grid-cols-[1fr_1fr_1fr_auto] px-3 py-2 text-sm ${
            index !== members.length - 1 ? "border-b border-gray-200" : ""
          }`}
        >
          <div className="self-center">
            {user.last_name} {user.first_name}
          </div>
          <div className="self-center">
            {user.position}
          </div>
          <div className="self-center">
            {user.department}, {user.faculty}
          </div>
          {showAction && (
            <RemoveTeamMemberButton
              teamId={teamId!}
              memberId={user.id}
              memberName={`${user.last_name} ${user.first_name}`}
            />
          )}
        </div>
      ))}
    </div>
  );
}
