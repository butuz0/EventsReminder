import {baseApiSlice} from "@/lib/redux/slices/baseApiSlice";
import {
  DepartmentDetailsResponse,
  DepartmentsListResponse,
  FacultiesListResponse,
  FacultyDetailsResponse
} from "@/types";

export const unitsApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAllFaculties: builder.query<FacultiesListResponse, void>({
      query: () => "/units/all-faculties/"
    }),
    getAllDepartments: builder.query<DepartmentsListResponse, void>({
      query: () => "/units/all-departments/"
    }),
    getDepartmentDetails: builder.query<DepartmentDetailsResponse, number>({
      query: (department_id) => `/units/department/${department_id}/`
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
  useGetDepartmentDetailsQuery,
  useGetFacultyDetailsQuery,
  useGetFacultyDepartmentsQuery,
} = unitsApiSlice;