import FacultyDetails from "@/components/units/FacultyDetails";


export default function FacultyPage({params}: { params: { faculty_id: string } }) {
  const facultyId = Number(params.faculty_id);
  
  return (
    <FacultyDetails facultyId={facultyId}/>
  );
}