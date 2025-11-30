import { apiClient } from './client';
import { Assessment, Payment } from '../types/payment';

export const paymentsApi = {
  async getAssessments(): Promise<Assessment[]> {
    return apiClient.get<Assessment[]>('/assessments/');
  },

  async getAssessmentById(id: number): Promise<Assessment> {
    return apiClient.get<Assessment>(`/assessments/${id}/`);
  },

  async getStudentAssessment(enrollmentId: number): Promise<Assessment> {
    return apiClient.get<Assessment>(`/assessments/enrollment/${enrollmentId}/`);
  },

  async createAssessment(enrollmentId: number): Promise<Assessment> {
    return apiClient.post<Assessment>('/assessments/', { enrollmentId });
  },

  async approveAssessment(id: number): Promise<Assessment> {
    return apiClient.post<Assessment>(`/assessments/${id}/approve/`, {});
  },

  async createPayment(data: {
    assessmentId: number;
    amount: number;
    paymentMethod: string;
    referenceNumber?: string;
  }): Promise<Payment> {
    return apiClient.post<Payment>('/payments/', data);
  },

  async getPayments(assessmentId?: number): Promise<Payment[]> {
    const endpoint = assessmentId 
      ? `/payments/?assessment=${assessmentId}` 
      : '/payments/';
    return apiClient.get<Payment[]>(endpoint);
  },

  async confirmPayment(id: number): Promise<Payment> {
    return apiClient.post<Payment>(`/payments/${id}/confirm/`, {});
  },
};
