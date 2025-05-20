import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  CreateRegistrationCardResponse,
  CreateUpdateRegistrationCardData,
  RegistrationCard,
  RegistrationCardsListResponse
} from "@/types";

export const registrationCardsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getRegistrationCards: builder.query<RegistrationCardsListResponse, void>({
      query: () => "/registration_cards/",
    }),
    getRegistrationCardDetails: builder.query<RegistrationCard, string>({
      query: (card_id) => `/registration_cards/${card_id}/`,
    }),
    createRegistrationCard: builder.mutation<CreateRegistrationCardResponse, CreateUpdateRegistrationCardData>({
      query: (data) => ({
        url: "/registration_cards/",
        method: "POST",
        body: data,
      }),
    }),
    updateRegistrationCard: builder.mutation<RegistrationCard, {
      card_id: string,
      data: CreateUpdateRegistrationCardData
    }>({
      query: ({card_id, data}) => ({
        url: `/registration_cards/${card_id}/`,
        method: "PATCH",
        body: data,
      }),
    }),
    deleteRegistrationCard: builder.mutation<void, string>({
      query: (card_id) => ({
        url: `/registration_cards/${card_id}/`,
        method: "DELETE",
      }),
    }),
  })
})

export const {
  useGetRegistrationCardsQuery,
  useGetRegistrationCardDetailsQuery,
  useCreateRegistrationCardMutation,
  useUpdateRegistrationCardMutation,
  useDeleteRegistrationCardMutation
} = registrationCardsApiSlice;