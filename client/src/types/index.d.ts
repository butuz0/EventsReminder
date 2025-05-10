export interface Faculty {
  id: number;
  faculty_name: string;
  faculty_abbreviation: string;
  num_employees: number;
}

export interface Department {
  id: number;
  department_name: string;
  department_abbreviation: string;
  faculty: number;
  num_employees: number;
}

export interface FacultyDetailsResponse {
  id: number;
  faculty_name: string;
  faculty_abbreviation: string;
  departments: Department[];
}

export interface FacultiesListResponse {
  status_code: number;
  faculties: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Faculty[];
  }
}

export interface DepartmentsListResponse {
  status_code: number;
  departments: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Department[];
  }
}

export interface RegisterUserData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  re_password: string;
}

export interface BaseUserResponse {
  first_name: string;
  last_name: string;
  email: string;
  id: string;
}

export interface ActivateUserData {
  uid: string;
  token: string;
}

export interface LoginUserData {
  email: string;
  password: string;
}

export interface ResetPasswordRequestData {
  email: string;
}

export interface ResetPasswordConfirmData {
  uid: string;
  token: string;
  new_password: string;
  re_new_password: string;
}
