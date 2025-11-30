export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  role: 'student' | 'registrar' | 'cashier' | 'admin';
  studentId?: string;
  createdAt: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  studentId?: string;
  role?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}
