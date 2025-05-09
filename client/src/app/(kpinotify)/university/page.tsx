"use client";

import PageTitle from "@/components/shared/PageTitle";
import FacultiesTable from "@/components/units/FacultiesTable";


export default function UniversityPage() {
  return (
    <div>
      <PageTitle title="Факультети"/>
      <FacultiesTable/>
    </div>
  );
}