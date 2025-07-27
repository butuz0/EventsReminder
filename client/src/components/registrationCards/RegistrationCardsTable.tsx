"use client";

import Link from "next/link";
import clsx from "clsx";
import {useGetRegistrationCardsQuery} from "@/lib/redux/slices/registrationCards/registrationCardsApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import React from "react";
import {formatDate} from "@/utils/formatDateTime";
import {Button} from "@/components/ui/button";

export default function RegistrationCardsTable() {
  const {data, isLoading, isError} = useGetRegistrationCardsQuery();
  
  if (isLoading) {
    return (
      <LoaderComponent
        size="lg"
        text="Завантаження реєстраційних карток АЦСК..."
        className="h-3/5"
      />
    );
  }
  
  if (isError || !data) {
    return (
      <div className="text-center text-red-600 font-medium">
        Не вдалося завантажити реєстраційні картки АЦСК.
      </div>
    );
  }
  
  const cards = data?.registration_cards.results;
  
  if (cards.length === 0) {
    return (
      <div className="text-center space-y-2">
        <div className="text-gray-600 font-medium">
          Реєстраційних карток АЦСК не знайдено
        </div>
        <Button asChild className="mb-2">
          <Link href={"/documents/registration-cards/create"}>
            Додати картку
          </Link>
        </Button>
      </div>
    );
  }
  
  return (
    <div>
      <div className="flex justify-between items-end mb-2">
        <p>Реєстраційні картки АЦСК</p>
        <Button asChild>
          <Link href={"/documents/registration-cards/create"}>
            Додати картку
          </Link>
        </Button>
      </div>
      
      <div className="rounded-xl bg-gray-100 p-2 shadow-lg border border-gray-200">
        <div className="grid grid-cols-[2fr_1fr_1fr_1fr] rounded-t-xl px-4 py-5 font-semibold text-sm">
          <div>Назва організації</div>
          <div>ПІБ</div>
          <div>Дата підписання</div>
          <div>Дата завершення дії</div>
        </div>
        
        <div className="divide-y-2 divide-gray-100 text-sm">
          {cards.map((card, i) => {
            const isFirst = i === 0;
            const isLast = i === cards.length - 1;
            
            return (
              <Link
                key={card.id}
                href={`/documents/registration-cards/${card.id}/`}
                className={clsx(
                  "grid grid-cols-[2fr_1fr_1fr_1fr] bg-white px-4 py-4 transition-colors hover:bg-gray-200",
                  {
                    "rounded-t-md": isFirst,
                    "rounded-b-md": isLast
                  }
                )}
              >
                <div className="truncate" title={card.organization_name}>
                  {card.organization_name || <span className="text-gray-400 italic">—</span>}
                </div>
                <div>
                  {card.full_name || <span className="text-gray-400 italic">—</span>}
                </div>
                <div>
                  {card.issue_date
                    ? formatDate(card.issue_date.toString())
                    : <span className="text-gray-400 italic">—</span>
                  }
                </div>
                <div>
                  {
                    card.expiration_date
                      ? formatDate(card.expiration_date.toString())
                      : <span className="text-gray-400 italic">—</span>
                  }
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
