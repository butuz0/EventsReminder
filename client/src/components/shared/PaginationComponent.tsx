"use client";

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import {useEffect, useState} from "react";
import {usePathname, useRouter, useSearchParams} from "next/navigation";

interface PaginationComponentProps {
  currentPage: number;
  totalPages: number;
}


export default function PaginationComponent({currentPage, totalPages}: PaginationComponentProps) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const {replace} = useRouter();
  const [activePage, setActivePage] = useState<number>(currentPage);
  
  useEffect(() => {
    setActivePage(Number(searchParams.get("page")) || 1);
  }, [searchParams]);
  
  const handlePageChange = (page: number) => {
    if (page < 1 || page > totalPages) return;
    
    const params = new URLSearchParams(searchParams);
    params.set("page", page.toString());
    replace(`${pathname}?${params.toString()}`);
  };
  
  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={() => handlePageChange(activePage - 1)}
            disabled={activePage <= 1}
          />
        </PaginationItem>
        
        <PaginationItem key={activePage}>
          <PaginationLink
            isActive
          >
            {activePage}
          </PaginationLink>
        </PaginationItem>
        
        <PaginationItem>
          <PaginationNext
            onClick={() => handlePageChange(activePage + 1)}
            disabled={activePage >= totalPages}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
