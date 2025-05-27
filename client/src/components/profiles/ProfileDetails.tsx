"use client";

import {useGetMyProfileQuery} from "@/lib/redux/slices/users/usersApiSlice";
import LoaderComponent from "@/components/shared/Loader";
import InfoBlock from "@/components/shared/InfoBlock";
import {PencilIcon} from "@heroicons/react/24/outline";
import {UserCircleIcon} from "@heroicons/react/24/solid";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import TelegramInfoBlock from "@/components/profiles/TelegramInfoBlock";
import AccountDeleteButton from "@/components/profiles/AccoutDeletionDialog";


export default function ProfileDetails() {
  const {data, isLoading, isError} = useGetMyProfileQuery();
  
  if (isLoading) {
    return (
      <LoaderComponent
        size="xl"
        text="Завантаження профілю..."
        className="h-3/4"
      />
    );
  }
  
  if (isError || !data) {
    return (
      <div className="text-center font-medium text-red-600">
        Не вдалося завантажити Ваш профіль. Спробуйте пізніше.
      </div>
    );
  }
  
  const {
    first_name,
    last_name,
    email,
    phone_number,
    gender,
    position,
    department_name,
    department_abbreviation,
    faculty,
    faculty_abbreviation,
    avatar_url,
    telegram_username,
    telegram_phone_number,
    is_telegram_verified,
  } = data.profile;
  
  
  return (
    <div className="w-full rounded-xl bg-gray-100
    p-5 shadow-md space-y-6 border border-gray-200">
      <div className="flex items-center gap-6
      rounded-lg bg-white p-6 shadow-md">
        <div className="h-32 w-32 overflow-hidden rounded-full
        border border-gray-300 bg-gray-50">
          {avatar_url ? (
            <img
              src={avatar_url}
              alt="Аватар"
              className="h-full w-full object-cover"
            />
          ) : (
            <UserCircleIcon className="w-full p-4 text-gray-500"/>
          )}
        </div>
        
        <div className="flex flex-col gap-1">
          <p className="text-2xl font-bold">
            {first_name} {last_name}
          </p>
          <p className="font-medium text-gray-800">
            {position}
          </p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Інститут / Факультет">
          <p>
            {faculty} ({faculty_abbreviation})
          </p>
        </InfoBlock>
        <InfoBlock label="Кафедра">
          <p>
            {department_name} ({department_abbreviation})
          </p>
        </InfoBlock>
      </div>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <InfoBlock label="Email">
          <p>
            {email}
          </p>
        </InfoBlock>
        <InfoBlock label="Телефон">
          <p>
            {phone_number || "Не вказано"}
          </p>
        </InfoBlock>
        <InfoBlock label="Стать">
          <p>
            {gender || "Не вказано"}
          </p>
        </InfoBlock>
      </div>
      
      <TelegramInfoBlock
        username={telegram_username}
        phoneNumber={telegram_phone_number}
        isVerified={is_telegram_verified}
      />
      
      <div className="flex justify-between">
        <AccountDeleteButton/>
        <Button asChild>
          <Link href="/profile/update/">
            <PencilIcon className="w-5"/>
            Оновити профіль
          </Link>
        </Button>
      </div>
    </div>
  );
}
