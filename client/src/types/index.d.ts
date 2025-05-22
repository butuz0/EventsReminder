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

export interface DepartmentDetailsResponse {
  id: number;
  department: Department;
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

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  gender: string;
  position: string;
  phone_number: string;
  telegram_username: string;
  telegram_phone_number: string;
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
  first_name: string,
  last_name: string,
  position: string,
  phone_number: string,
  telegram_username: string,
  telegram_phone_number: string,
  avatar_url: string,
  is_telegram_verified: boolean,
  id: string,
  email: string,
  gender: string,
  department: string,
  department_name: string,
  department_abbreviation: string,
  faculty: string,
  faculty_abbreviation: string
}

export interface MyProfileResponse {
  status_code: number;
  profile: Profile;
}

export interface AllProfilesResponse {
  status_code: number;
  profiles: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Profile[];
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

export interface Event {
  id: string,
  created_by: BaseUserResponse,
  title: string,
  description: string,
  start_datetime: string,
  location: string,
  link: string,
  priority: number,
  image_url: string,
  tags: string[],
  team: {
    id: string,
    name: string
  }
  assigned_to: BaseUserResponse[],
  is_recurring: boolean,
  recurring_event: {
    id: string,
    recurrence_rule: string,
    recurrence_end_datetime: string,
    created_at: string,
    updated_at: string
  }
}

export interface MyEventsResponse {
  status_code: number,
  events: {
    count: number,
    next: string,
    previous: string,
    results: Event[]
  }
}

export interface EventDetailsResponse {
  status_code: number,
  event: Event
}

export interface CreateUpdateEventData {
  title: string,
  description?: string,
  start_datetime: string | Date,
  location?: string,
  link?: string,
  priority: number,
  image?: string | File,
  tags?: string[],
  assigned_to?: string[],
  is_recurring?: boolean
}

export interface CreateUpdateEventResponse {
  status_code: number,
  event: Event
}

export interface CreateUpdateRecurringEventData {
  recurrence_rule: string,
  recurrence_end_datetime?: string
}

export interface CreateUpdateRecurringEventResponse {
  status_code: number,
  recurring_event: {
    id: string,
    recurrence_rule: string,
    recurrence_end_datetime: string,
    created_at: string,
    updated_at: string
  }
}

export interface Team {
  id: string,
  name: string,
  description: string,
  created_by: BaseUserResponse,
  members: BaseUserResponse[],
  created_at: string,
  updated_at: string
}


export interface MyTeamsResponse {
  status_code: number,
  teams: {
    count: number,
    next: string,
    previous: string,
    results: Team[]
  }
}

export interface TeamDetailsResponse {
  status_code: number,
  team: Team
}

export interface TeamsMembersResponse {
  status_code: number,
  next: null,
  previous: null,
  results: BaseUserResponse[]
}

export interface CreateTeamData {
  name: string,
  description?: string,
  members_ids?: string[]
}

export interface CreateTeamResponse {
  status_code: number,
  team: Team
}

export interface UpdateTeamData {
  name?: string,
  description?: string,
}

export interface UpdateTeamResponse {
  status_code: number,
  team: {
    name: string,
    description: string,
  }
}

export interface Invitation {
  id: string,
  created_by: BaseUserResponse,
  team_name: string,
  team_description: string,
  sent_to: BaseUserResponse,
  status: string,
  created_at: string,
  updated_at: string,
}

export interface MyInvitationsResponse {
  status_code: number,
  invitations: {
    count: number,
    next: string,
    previous: string,
    results: Invitation[]
  }
}

export interface InvitationDetailsResponse {
  status_code: number,
  invitations: Invitation
}

export interface CreateInvitationData {
  team: string,
  sent_to: string,
}

export interface CreateInvitationResponse {
  status_code: number,
  invitations: Invitation
}

export interface RespondToInvitationData {
  status: string,
}

export interface Notification {
  id: number,
  event: string,
  notification_method: string,
  created_by: string,
  notification_datetime: string,
  is_sent: boolean,
}

export interface NotificationCreateData {
  event: string,
  notification_method: string,
  notification_datetime: string | Date,
}

export interface NotificationResponse {
  status_code: number,
  notifications: Notification[]
}

export interface NotificationsListResponse {
  status_code: number,
  notifications: {
    count: number,
    next: string,
    previous: string,
    results: Notification[]
  }
}

export interface RegistrationCard {
  id: string,
  created_at: string,
  updated_at: string,
  organization_name: string,
  edrpou_code: string,
  region: string,
  city: string,
  full_name: string,
  id_number: string,
  keyword_phrase: string,
  voice_phrase: string,
  email: string,
  phone_number: string,
  electronic_seal_name: string,
  electronic_seal_keyword_phrase: string,
}

export interface CreateUpdateRegistrationCardData {
  organization_name: string,
  edrpou_code?: string,
  region?: string,
  city?: string,
  full_name?: string,
  id_number?: string,
  keyword_phrase?: string,
  voice_phrase?: string,
  email?: string,
  phone_number?: string,
  electronic_seal_name?: string,
  electronic_seal_keyword_phrase?: string,
}

export interface CreateRegistrationCardResponse {
  status_code: number,
  registration_card: RegistrationCard
}

export interface RegistrationCardsListResponse {
  status_code: number,
  registration_cards: {
    count: number,
    next: string,
    previous: string,
    results: RegistrationCard[]
  }
}