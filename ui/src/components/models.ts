export interface ChatMessage {
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
