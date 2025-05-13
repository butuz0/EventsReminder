import React from "react";

export default function InfoBlock({label, value}: { label: string; value: React.ReactNode }) {
  return (
    <div className="rounded-xl bg-white p-4 shadow-md">
      <div className="text-sm text-gray-700">{label}</div>
      <div className="text-lg font-medium">{value}</div>
    </div>
  )
}
