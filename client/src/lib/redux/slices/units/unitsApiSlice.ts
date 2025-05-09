import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {DepartmentsListResponse, FacultiesListResponse, FacultyDetailsResponse} from "@/types";

export const unitsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAllFaculties: builder.query<FacultiesListResponse, void>({
      query: () => "/units/all-faculties/"
    }),
    getAllDepartments: builder.query<DepartmentsListResponse, void>({
      query: () => "/units/all-departments/"
    }),
    getFacultyDetails: builder.query<FacultyDetailsResponse, number>({
      query: (faculty_id) => `/units/faculty/${faculty_id}/`
    }),
    getFacultyDepartments: builder.query<DepartmentsListResponse, number>({
      query: (faculty_id) => `/units/faculty/${faculty_id}/departments/`
    }),
  }),
});

export const {
  useGetAllFacultiesQuery,
  useGetAllDepartmentsQuery,
  useGetFacultyDetailsQuery,
  useGetFacultyDepartmentsQuery,
} = unitsApiSlice;