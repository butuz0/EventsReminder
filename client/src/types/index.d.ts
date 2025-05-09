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
