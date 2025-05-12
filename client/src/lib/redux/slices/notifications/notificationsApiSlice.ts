import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  NotificationCreateData,
  NotificationResponse,
  NotificationsListResponse
} from "@/types";

export const eventsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    createNotification: builder.mutation<NotificationResponse, NotificationCreateData>({
      query: (data) => ({
        url: "/notifications/create/",
        method: "POST",
        body: data,
        providesTags: ["Notifications"],
      }),
    }),
    getAllNotifications: builder.query<NotificationsListResponse, void>({
      query: () => "/notifications/",
      providesTags: ["Notifications"],
    }),
    eventNotifications: builder.query<NotificationsListResponse, string>({
      query: (event_id) => `/notifications/event/${event_id}/`,
      providesTags: ["Notifications"],
    }),
    deleteNotification: builder.mutation<void, number>({
      query: (notification_id) => ({
        url: `/notifications/delete/${notification_id}/`,
        method: "DELETE"
      }),
      invalidatesTags: ["Notifications"],
    }),
  })
});

export const {
  useCreateNotificationMutation,
  useGetAllNotificationsQuery,
  useEventNotificationsQuery,
  useDeleteNotificationMutation,
} = eventsApiSlice;