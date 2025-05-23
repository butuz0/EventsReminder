import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  AllProfilesResponse,
  MyProfileResponse,
  SetupProfileData,
  UpdateProfileData,
  UpdateProfileResponse
} from "@/types";

export const usersApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    setupProfile: builder.mutation<void, SetupProfileData>({
      query: (data) => ({
        url: "/profiles/my-profile/setup/",
        method: "PUT",
        body: data,
      }),
      invalidatesTags: ["User"],
    }),
    getMyProfile: builder.query<MyProfileResponse, void>({
      query: () => "/profiles/my-profile/",
      providesTags: ["User"],
    }),
    getAllProfiles: builder.query<AllProfilesResponse, Record<string, any>>({
      query: (params) => ({
        url: "/profiles/",
        params,
      }),
      providesTags: ["User"],
    }),
    updateProfile: builder.mutation<UpdateProfileResponse, UpdateProfileData | FormData>({
      query: (data) => ({
        url: "/profiles/my-profile/update/",
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: ["User"],
    })
  }),
});

export const {
  useSetupProfileMutation,
  useGetMyProfileQuery,
  useGetAllProfilesQuery,
  useUpdateProfileMutation,
} = usersApiSlice;
