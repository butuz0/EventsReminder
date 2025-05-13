import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {setLogin, setLogout} from "@/lib/redux/slices/auth/authSlice";
import {BaseQueryFn, FetchArgs, FetchBaseQueryError,} from "@reduxjs/toolkit/query";
import {Mutex} from "async-mutex";


const mutex = new Mutex();

const baseQuery = fetchBaseQuery({
  baseUrl: "/api/v1",
  credentials: "include",
});

const baseQueryWithReauth: BaseQueryFn<
  string | FetchArgs,
  unknown,
  FetchBaseQueryError
> = async (args, api, extraOptions) => {
  await mutex.waitForUnlock();
  
  let response = await baseQuery(args, api, extraOptions);
  
  if (response.error && response.error.status === 401) {
    if (!mutex.isLocked()) {
      const release = await mutex.acquire();
      try {
        const refreshResponse = await baseQuery(
          {
            url: "/auth/refresh/",
            method: "POST",
          },
          api,
          extraOptions,
        );
        
        if (refreshResponse?.data) {
          api.dispatch(setLogin());
          response = await baseQuery(args, api, extraOptions);
        } else {
          api.dispatch(setLogout());
        }
      } finally {
        release();
      }
    } else {
      await mutex.waitForUnlock();
      response = await baseQuery(args, api, extraOptions);
    }
  }
  
  return response;
};


export const baseApiSlice = createApi({
  reducerPath: "api",
  baseQuery: baseQueryWithReauth,
  endpoints: (builder) => ({}),
  tagTypes: ["User", "Events", "Notifications", "Teams", "Invitations"],
});
