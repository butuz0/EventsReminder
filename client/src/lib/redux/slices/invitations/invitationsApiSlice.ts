import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  CreateInvitationData,
  CreateInvitationResponse,
  InvitationDetailsResponse,
  MyInvitationsResponse
} from "@/types";

export const invitationsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMyInvitations: builder.query<MyInvitationsResponse, void>({
      query: () => "/teams/invitations/",
      providesTags: ["Invitations"]
    }),
    getTeamInvitations: builder.query<MyInvitationsResponse, string>({
      query: (teamId) => `/teams/${teamId}/invitations/`,
      providesTags: ["Invitations"]
    }),
    getInvitationDetails: builder.query<InvitationDetailsResponse, string>({
      query: (invitationId) => `/teams/invitations/${invitationId}/`,
      providesTags: ["Invitations"]
    }),
    createInvitation: builder.mutation<CreateInvitationResponse, CreateInvitationData>({
      query: (data) => ({
        url: "/teams/invitations/create/",
        method: "POST",
        body: data
      }),
      invalidatesTags: ["Invitations"]
    }),
    respondToInvitation: builder.mutation<string, { invitationId: string, status: string }>({
      query: ({invitationId, status}) => ({
        url: `/teams/invitations/${invitationId}/respond/`,
        method: "PATCH",
        body: {"status": status}
      }),
      invalidatesTags: ["Invitations"]
    }),
    deleteInvitation: builder.mutation<void, string>({
      query: (invitationId) => ({
        url: `/teams/invitations/${invitationId}/delete/`,
        method: "DELETE"
      }),
      invalidatesTags: ["Invitations"]
    }),
  }),
});

export const {
  useGetMyInvitationsQuery,
  useGetTeamInvitationsQuery,
  useGetInvitationDetailsQuery,
  useCreateInvitationMutation,
  useRespondToInvitationMutation,
  useDeleteInvitationMutation,
} = invitationsApiSlice;