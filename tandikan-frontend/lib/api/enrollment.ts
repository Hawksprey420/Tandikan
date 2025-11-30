import { apiClient } from './client';
import { Enrollment, Schedule, EnrolledSubject } from '../types/enrollment';

export const enrollmentApi = {
  async getEnrollments(): Promise<Enrollment[]> {
    return apiClient.get<Enrollment[]>('/enrollments/');
  },

  async getEnrollmentById(id: number): Promise<Enrollment> {
    return apiClient.get<Enrollment>(`/enrollments/${id}/`);
  },

  async getCurrentEnrollment(): Promise<Enrollment> {
    return apiClient.get<Enrollment>('/enrollments/current/');
  },

  async createEnrollment(data: {
    academicYear: string;
    semester: number;
    scheduleIds: number[];
  }): Promise<Enrollment> {
    return apiClient.post<Enrollment>('/enrollments/', data);
  },

  async updateEnrollment(id: number, data: Partial<Enrollment>): Promise<Enrollment> {
    return apiClient.put<Enrollment>(`/enrollments/${id}/`, data);
  },

  async approveEnrollment(id: number): Promise<Enrollment> {
    return apiClient.post<Enrollment>(`/enrollments/${id}/approve/`, {});
  },

  async rejectEnrollment(id: number, reason: string): Promise<Enrollment> {
    return apiClient.post<Enrollment>(`/enrollments/${id}/reject/`, { reason });
  },

  async dropSubject(enrollmentId: number, subjectId: number): Promise<void> {
    return apiClient.delete(`/enrollments/${enrollmentId}/subjects/${subjectId}/`);
  },

  async getAvailableSchedules(yearLevel: number, semester: number): Promise<Schedule[]> {
    return apiClient.get<Schedule[]>(`/schedules/?year_level=${yearLevel}&semester=${semester}`);
  },
};
