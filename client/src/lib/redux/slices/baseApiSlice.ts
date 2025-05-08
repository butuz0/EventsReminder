import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

const baseQuery = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({baseUrl: "/api/v1", credentials: "include"}),
  endpoints: (builder) => ({})
});
