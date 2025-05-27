"use client";

import {useGetAllNotificationsQuery} from "@/lib/redux/slices/notifications/notificationsApiSlice";
import {dateTimeDistanceToNow} from "@/utils/formatDateTime";
import InfoBlock from "@/components/shared/InfoBlock";


export default function UpcomingRemindersCard() {
  const {data, isLoading} = useGetAllNotificationsQuery();
  
  const reminders = (data?.notifications.results ?? [])
    .filter((n) => new Date(n.notification_datetime) >= new Date())
    .sort((a, b) => new Date(a.notification_datetime).getTime() - new Date(b.notification_datetime).getTime())
    .slice(0, 3);
  
  return (
    <InfoBlock label="Найближчі нагадування">
      {isLoading ? (
        <p>Завантаження...</p>
      ) : reminders.length === 0 ? (
        <p>Немає запланованих нагадувань</p>
      ) : (
        reminders.map((n) => (
          <div key={n.id}>
            <strong>{dateTimeDistanceToNow(n.notification_datetime)}:</strong> {n.notification_method === "telegram" ? "Telegram" : "Email"}
          </div>
        ))
      )}
    </InfoBlock>
  );
}
