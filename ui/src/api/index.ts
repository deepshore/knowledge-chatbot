import { api } from 'boot/axios';
import { DeepshoreChatRequest, DeepshoreChatResponse } from 'src/types/chat';
import { AppSettings } from '../types/appsettings';

export async function sendQuestion(
  data: DeepshoreChatRequest
): Promise<DeepshoreChatResponse> {
  const response = await api.post('/chatbot', data);
  return response.data;
}

export async function getAppSettings(): Promise<AppSettings> {
  const response = await api.get('/disclaimer');
  return response.data;
}
