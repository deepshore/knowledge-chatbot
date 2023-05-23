interface DeepshoreChatMessage {
  id: number;
  text: string;
  name: string;
  stamp: string;
  avatar?: string;
  textColor?: string;
  bgColor?: string;
  sent: boolean;
  textHtml: boolean;
}

interface DeepshoreChatRequest {
  question: string;
  timestamp?: string;
}

interface DeepshoreChatResponse {
  origin?: DeepshoreChatRequest;
  answer: string;
  related_articles: Array<string>;
  error?: string;
  timestamp?: string;
}

export { DeepshoreChatMessage, DeepshoreChatRequest, DeepshoreChatResponse };
