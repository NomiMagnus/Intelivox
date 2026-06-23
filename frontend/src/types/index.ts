export interface UserRole {
  id: string
  role_id: string
  code?: string
  name?: string
  start_date?: string | null
  end_date?: string | null
  status: string
}

export interface User {
  id: string
  id_number: string
  first_name?: string
  last_name?: string
  username: string
  email: string
  phone?: string
  department?: string
  status: string
  must_change_password: boolean
  created_at?: string
  roles: UserRole[]
}

export interface Role {
  id: string
  code: string
  name?: string
  status: string
}

export interface MeResponse {
  user: User
  is_admin: boolean
}

export interface LoginCredentials {
  username_or_email: string
  password: string
}

export interface ChangePasswordPayload {
  old_password: string
  new_password: string
}

export interface UserCreatePayload {
  id_number: string
  username: string
  email: string
  first_name?: string
  last_name?: string
  phone?: string
  department?: string
  role_codes?: string[]
}

export interface Resident {
  id: string
  first_name: string
  last_name: string
  status: string
  mobile_phone?: string
  home_phone?: string
  work_phone?: string
  email?: string
  type?: string
}

export interface ResidentSearchQuery {
  term: string
}
