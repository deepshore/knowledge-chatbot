import { api } from 'boot/axios';

export interface DeepshoreChatRequest {
  question: string;
  timestamp?: string;
}

export interface DeepshoreChatResponse {
  origin?: DeepshoreChatRequest;
  answer: string;
  related_articles: Array<string>;
  error?: string;
  timestamp?: string;
}

export async function sendQuestion(
  data: DeepshoreChatRequest
): Promise<DeepshoreChatResponse> {
  const response = await api.post('http://0.0.0.0:8080/chatbot', data);
  return response.data;
}
