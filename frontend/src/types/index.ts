export interface User {
  id: string
  name: string
  email: string
  role: string
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
