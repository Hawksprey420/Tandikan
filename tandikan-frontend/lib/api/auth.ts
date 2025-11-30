import { apiClient } from './client';
import { LoginCredentials, RegisterData, AuthResponse, User } from '../types/auth';

export const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login/', credentials);
    apiClient.setToken(response.token);
    return response;
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register/', data);
    apiClient.setToken(response.token);
    return response;
  },

  async logout(): Promise<void> {
    await apiClient.post('/auth/logout/', {});
    apiClient.clearToken();
  },

  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me/');
  },

  async refreshToken(): Promise<{ token: string }> {
    return apiClient.post('/auth/refresh/', {});
  },
};
