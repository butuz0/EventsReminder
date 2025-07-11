"use client";

import React, {useEffect, useState} from "react";


export default function ClientOnlyComponent({children}: { children: React.ReactNode }) {
  const [hasMounted, setHasMounted] = useState(false);
  
  useEffect(() => {
    setHasMounted(true);
  }, []);
  
  if (!hasMounted) return <p>Завантаження...</p>;
  
  return <>{children}</>;
}