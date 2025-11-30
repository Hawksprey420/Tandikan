export interface Student {
  id: number;
  studentId: string;
  firstName: string;
  lastName: string;
  middleName?: string;
  email: string;
  phone: string;
  dateOfBirth: string;
  address: string;
  yearLevel: number;
  program: string;
  status: 'active' | 'inactive' | 'graduated';
  enrolledAt: string;
}

export interface StudentProfile extends Student {
  currentEnrollment?: Enrollment;
  totalUnits: number;
  gpa?: number;
}
