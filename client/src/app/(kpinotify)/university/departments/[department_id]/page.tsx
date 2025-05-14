import DepartmentDetails from "@/components/units/DepartmentDetails";

interface DepartmentDetailsPageProps {
  params: {
    department_id: number
  }
}


export default function DepartmentDetailsPage({params}: DepartmentDetailsPageProps) {
  const departmentId = params.department_id;
  
  return (
    <DepartmentDetails departmentId={departmentId}/>
  )
}