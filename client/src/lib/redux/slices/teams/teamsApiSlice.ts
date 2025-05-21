import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  TeamsMembersResponse,
  MyTeamsResponse,
  TeamDetailsResponse,
  CreateTeamData,
  CreateTeamResponse,
  UpdateTeamResponse,
  UpdateTeamData,
  EventDetailsResponse,
  MyEventsResponse
} from "@/types";

export const teamsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMyTeams: builder.query<MyTeamsResponse, void>({
      query: () => "/teams/",
      providesTags: ["Teams"]
    }),
    getTeamDetails: builder.query<TeamDetailsResponse, string>({
      query: (teamId) => `/teams/${teamId}/`,
      providesTags: ["Teams"]
    }),
    getTeamMembers: builder.query<TeamsMembersResponse, string>({
      query: (teamId) => `/teams/${teamId}/members/`,
      providesTags: ["Teams"]
    }),
    getTeamEvents: builder.query<MyEventsResponse, string>({
      query: (teamId) => `/teams/${teamId}/events/`,
      providesTags: ["Teams", "Events"]
    }),
    createTeam: builder.mutation<CreateTeamResponse, CreateTeamData>({
      query: (data) => ({
        url: "/teams/create/",
        method: "POST",
        body: data
      }),
      invalidatesTags: ["Teams"]
    }),
    updateTeam: builder.mutation<UpdateTeamResponse, { teamId: string, data: UpdateTeamData }>({
      query: ({teamId, data}) => ({
        url: `/teams/${teamId}/update/`,
        method: "PATCH",
        body: data
      }),
      invalidatesTags: ["Teams"]
    }),
    removeMember: builder.mutation<void, { teamId: string, memberId: string }>({
      query: ({teamId, memberId}) => ({
        url: `/teams/${teamId}/remove-member/${memberId}/`,
        method: "DELETE"
      }),
      invalidatesTags: ["Teams"]
    }),
    deleteTeam: builder.mutation<void, string>({
      query: (teamId) => ({
        url: `/teams/${teamId}/delete/`,
        method: "DELETE"
      }),
      invalidatesTags: ["Teams"]
    }),
    leaveTeam: builder.mutation<void, string>({
      query: (teamId) => ({
        url: `/teams/${teamId}/leave/`,
        method: "DELETE"
      }),
      invalidatesTags: ["Teams"]
    }),
  })
})

export const {
  useGetMyTeamsQuery,
  useGetTeamDetailsQuery,
  useGetTeamMembersQuery,
  useGetTeamEventsQuery,
  useCreateTeamMutation,
  useUpdateTeamMutation,
  useDeleteTeamMutation,
  useLeaveTeamMutation,
} = teamsApiSlice;