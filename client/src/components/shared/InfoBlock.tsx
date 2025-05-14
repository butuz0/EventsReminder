import React from "react";

interface InfoBlockProps {
  label: string,
  children: React.ReactNode
}


export default function InfoBlock({label, children}: InfoBlockProps) {
  return (
    <div className="rounded-xl bg-white p-4 shadow-md">
      <div className="text-sm text-gray-800">{label}</div>
      <div className="text-lg font-medium">
        {children}
      </div>
    </div>
  )
}
