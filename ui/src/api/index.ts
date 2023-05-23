import { api } from 'boot/axios';
import { DeepshoreChatRequest, DeepshoreChatResponse } from 'src/types/chat';

export async function sendQuestion(
  data: DeepshoreChatRequest
): Promise<DeepshoreChatResponse> {
  const response = await api.post('http://0.0.0.0:8080/chatbot', data);
  return response.data;
}
