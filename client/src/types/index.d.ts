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

export interface Profile {
  "first_name": string,
  "last_name": string,
  "position": string,
  "phone_number": string,
  "telegram_username": string,
  "telegram_phone_number": string,
  "avatar_url": string,
  "is_telegram_verified": boolean,
  "id": string,
  "email": string,
  "gender": string,
  "department": string,
  "department_abbreviation": string,
  "faculty": string,
  "faculty_abbreviation": string
}

export interface MyProfileResponse {
  status_code: number;
  profile: Profile;
}

export interface AllProfilesResponse {
  status_code: number;
  results: {
    count: number;
    next: string | null;
    previous: string | null;
    profiles: Profile[];
  }
}

export interface UpdateProfileData {
  first_name: string;
  last_name: string;
  position: string;
  phone_number?: string;
  telegram_username?: string;
  telegram_phone_number?: string;
  avatar?: string;
  gender: string;
  department: number;
}

export interface UpdateProfileResponse {
  status_code: number;
  profile: {
    first_name: string;
    last_name: string;
    position: string;
    phone_number: string;
    telegram_username: string;
    telegram_phone_number: string;
    avatar_url: string;
    gender: string;
    department: number;
  }
}

export interface SetupProfileData {
  position: string;
  gender: string;
  department: number;
}