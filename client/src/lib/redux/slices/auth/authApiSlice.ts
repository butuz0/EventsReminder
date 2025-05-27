import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  ActivateUserData,
  BaseUserResponse,
  LoginUserData,
  RegisterUserData,
  ResetPasswordConfirmData,
  ResetPasswordRequestData,
  User
} from "@/types";


export const authApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    registerUser: builder.mutation<BaseUserResponse, RegisterUserData>({
      query: (userData) => ({
        url: "/auth/users/",
        method: "POST",
        body: userData,
      }),
    }),
    activateUser: builder.mutation<void, ActivateUserData>({
      query: (credentials) => ({
        url: "/auth/users/activation/",
        method: "POST",
        body: credentials,
      }),
    }),
    loginUser: builder.mutation<void, LoginUserData>({
      query: (credentials) => ({
        url: "/auth/login/",
        method: "POST",
        body: credentials,
      }),
    }),
    logoutUser: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout/",
        method: "POST",
      }),
    }),
    resetPasswordRequest: builder.mutation<void, ResetPasswordRequestData>({
      query: (formData) => ({
        url: "/auth/users/reset_password/",
        method: "POST",
        body: formData,
      }),
    }),
    resetPasswordConfirm: builder.mutation<void, ResetPasswordConfirmData>({
      query: (formData) => ({
        url: "/auth/users/reset_password_confirm/",
        method: "POST",
        body: formData,
      }),
    }),
    refreshJWT: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/refresh/",
        method: "POST",
      }),
    }),
    getCurrentUser: builder.query<User, void>({
      query: () => "/auth/users/me/",
      providesTags: ["User"]
    }),
    deleteCurrentUser: builder.mutation<void, string>({
      query: (current_password) => ({
        url: "/auth/users/me/",
        body: {current_password: current_password},
        method: "DELETE",
      }),
    }),
  }),
});

export const {
  useRegisterUserMutation,
  useLoginUserMutation,
  useActivateUserMutation,
  useResetPasswordRequestMutation,
  useResetPasswordConfirmMutation,
  useLogoutUserMutation,
  useRefreshJWTMutation,
  useGetCurrentUserQuery,
  useDeleteCurrentUserMutation,
} = authApiSlice;