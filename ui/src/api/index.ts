import { api } from 'boot/axios';
import { DeepshoreChatRequest, DeepshoreChatResponse } from 'src/types/chat';
import { AppSettings } from '../types/appsettings';

export async function sendQuestion(
  data: DeepshoreChatRequest
): Promise<DeepshoreChatResponse> {
  try{
    const response = await api.post('/chatbot', data);
    return response.data;
  } catch (e) {
    return { 'error': JSON.stringify(e), 'answer': '', 'related_articles': [] }
  }
}

export async function getAppSettings(): Promise<AppSettings> {
  const response = await api.get('/appsettings');
  return response.data;
}
