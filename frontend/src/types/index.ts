export interface User {
  id: string
  name: string
  email: string
  role: string
}

export interface Resident {
  id: string
  firstName: string
  lastName: string
  room: string
  status: string
  notes?: string
}

export interface ResidentSearchQuery {
  term: string
}
