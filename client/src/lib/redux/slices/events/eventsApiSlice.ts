import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  CreateUpdateEventData,
  CreateUpdateEventResponse,
  EventDetailsResponse,
  MyEventsResponse,
  CreateUpdateRecurringEventData,
  CreateUpdateRecurringEventResponse
} from "@/types";

export const eventsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMyEvents: builder.query<MyEventsResponse, Record<string, any>>({
      query: (params) => ({
        url: "/events/",
        params,
      }),
      providesTags: ["Events"],
    }),
    getEventDetails: builder.query<EventDetailsResponse, string>({
      query: (event_id) => `/events/${event_id}/`,
      providesTags: ["Events"],
    }),
    createEvent: builder.mutation<CreateUpdateEventResponse, CreateUpdateEventData | FormData>({
      query: (data) => ({
        url: "/events/create/",
        method: "POST",
        body: data,
        providesTags: ["Events"],
      }),
    }),
    updateEvent: builder.mutation<CreateUpdateEventResponse, {
      event_id: string,
      data: CreateUpdateEventData | FormData
    }>({
      query: ({event_id, data}) => ({
        url: `/events/update/${event_id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: ["Events"],
    }),
    createRecurringEvent: builder.mutation<CreateUpdateRecurringEventResponse, {
      event_id: string,
      data: CreateUpdateRecurringEventData
    }>({
      query: ({event_id, data}) => ({
        url: `/events/${event_id}/recurring/create/`,
        method: "POST",
        body: data,
      }),
      invalidatesTags: ["Events"],
    }),
    updateRecurringEvent: builder.mutation<CreateUpdateRecurringEventResponse, {
      event_id: string,
      data: CreateUpdateRecurringEventData
    }>({
      query: ({event_id, data}) => ({
        url: `/events/${event_id}/recurring/update/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: ["Events"],
    }),
    deleteEvent: builder.mutation<void, string>({
      query: (event_id) => ({
        url: `/events/delete/${event_id}`,
        method: "DELETE"
      }),
      invalidatesTags: ["Events"],
    }),
    leaveEvent: builder.mutation<void, string>({
      query: (event_id) => ({
        url: `/events/leave/${event_id}`,
        method: "DELETE"
      }),
      invalidatesTags: ["Events"],
    }),
  })
});

export const {
  useGetMyEventsQuery,
  useGetEventDetailsQuery,
  useCreateEventMutation,
  useUpdateEventMutation,
  useCreateRecurringEventMutation,
  useUpdateRecurringEventMutation,
  useDeleteEventMutation,
  useLeaveEventMutation
} = eventsApiSlice;
