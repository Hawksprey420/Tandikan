export interface Subject {
  id: number;
  code: string;
  title: string;
  description: string;
  units: number;
  yearLevel: number;
  semester: number;
  prerequisites?: string[];
}

export interface Schedule {
  id: number;
  subject: Subject;
  section: string;
  instructor: string;
  days: string[];
  timeStart: string;
  timeEnd: string;
  room: string;
  maxSlots: number;
  availableSlots: number;
}

export interface EnrolledSubject {
  id: number;
  schedule: Schedule;
  enrolledAt: string;
  grade?: number;
  status: 'enrolled' | 'dropped' | 'completed';
}

export interface Enrollment {
  id: number;
  student: number;
  academicYear: string;
  semester: number;
  subjects: EnrolledSubject[];
  totalUnits: number;
  status: 'pending' | 'approved' | 'rejected' | 'completed';
  createdAt: string;
  approvedAt?: string;
}
