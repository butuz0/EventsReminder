"use client";

import {dateTimeDistanceToNow, formatDateTime} from "@/utils/formatDateTime";
import {NotificationMethods} from "@/constants";
import {Button} from "@/components/ui/button";
import React from "react";
import InfoBlock from "@/components/shared/InfoBlock";
import {
  useDeleteNotificationMutation,
  useEventNotificationsQuery
} from "@/lib/redux/slices/notifications/notificationsApiSlice";
import {toast} from "react-toastify";
import NotificationCreateForm from "@/components/forms/notifications/NotificationCreateForm";
import extractErrorMessage from "@/utils/extractErrorMessage";

interface NotificationsListProps {
  contentType: string;
  objectId: string;
}


export default function NotificationsList({contentType, objectId}: NotificationsListProps) {
  const {data, refetch} = useEventNotificationsQuery(objectId);
  const [deleteNotification] = useDeleteNotificationMutation();
  
  const notifications = data?.notifications.results;
  
  const deleteNotificationButton = async (notificationId: number) => {
    try {
      await toast.promise(deleteNotification(notificationId).unwrap(), {
        pending: "Видаляємо нагадування...",
        success: "Нагадування видалено!"
      });
    } catch (error) {
      toast.error(`Помилка під час видалення нагадування: ${extractErrorMessage(error)}`);
    }
  }
  
  return (
    <InfoBlock label="Нагадування">
      <div className="flex flex-col gap-3">
        {notifications && notifications.length > 0 &&
          notifications.map(n => (
            <div key={n.id} className="grid grid-cols-[5fr_2fr_1fr] gap-4">
              <p>
                {`${formatDateTime(n.notification_datetime)} - ${dateTimeDistanceToNow(n.notification_datetime)}`}
              </p>
              <p>
                {NotificationMethods.find(method => method.value === n.notification_method)?.label || "Невідомо"}
              </p>
              <Button
                variant="secondary"
                className="border border-red-400 bg-red-100
                    text-red-600 hover:cursor-pointer hover:bg-red-200"
                onClick={() => deleteNotificationButton(n.id)}
              >
                Видалити
              </Button>
            </div>
          ))}
        <NotificationCreateForm
          contentType={contentType}
          objectId={objectId}
          onSuccess={() => refetch()}
        />
      </div>
    </InfoBlock>
  )
}