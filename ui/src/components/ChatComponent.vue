<template>
  <div class="row justify-center chat-row">
    <div class="chat-div">
      <q-chat-message :label="chatLabel" role="heading" aria-level="1" />
      <q-chat-message
        v-for="msg in chat"
        :key="msg.id"
        :name="msg.name"
        :text="[msg.text]"
        :stamp="msg.stamp"
        :avatar="msg.avatar"
        :sent="msg.sent"
        :text-html="msg.textHtml"
        size="5"
      >
        <q-spinner-dots v-if="msg.text.length == 0" size="md" />
        <div
          v-if="msg.text.length > 0 && msg.textHtml == true"
          v-html="msg.text"
        ></div>
        <div v-if="msg.text.length > 0 && msg.textHtml == false">
          {{ msg.text }}
        </div>
      </q-chat-message>
    </div>
    <div class="chat-input-div">
      <q-input
        outlined
        v-model="message"
        placeholder="Nachricht"
        @keyup.enter="addMessage"
      >
        <template v-slot:after>
          <q-btn
            title="Nachricht abschicken"
            color="primary"
            round
            dense
            flat
            icon="send"
            @click="addMessage"
            :disable="isDisabled"
          />
        </template>
      </q-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, Ref } from 'vue';
import { date } from 'quasar';
import { sendQuestion } from 'src/api/index';
import {
  DeepshoreChatMessage,
  DeepshoreChatRequest,
  DeepshoreChatResponse
} from 'src/types/chat';

// data
let message = ref('');
let chat: Ref<Array<DeepshoreChatMessage>> = ref([]);
let blockedAPI = ref(false);
const errMessages = [
  'Ich habe die Frage leider nicht verstanden. Bitte versuche es mit einer anderen Formulierung.',
  'Ich habe leider keine Antwort parat. Kannst du die Frage anders formulieren?',
  'Tut mir leid, aber ich kann deine Frage leider nicht beantworten. Bitte versuche es mit einer anderen Formulierung.',
  'Könntest du die Frage bitte noch einmal anders formulieren?'
];

// computed
const isDisabled = computed(() => {
  // Prevent empty msg
  if (message.value.length == 0) {
    return true;
  }
  // Prevent multiple open requests
  if (blockedAPI.value) {
    return true;
  }
  return false;
});

const chatLabel = computed(() => {
  const timeStamp = Date.now();
  return `Chat: ${date.formatDate(timeStamp, 'ddd, DD.MM.YY')}`;
});

// Methods

/**
 * Add user question to chat, get answer from chatbot backend and add that answer to chat.
 */
async function addMessage(): Promise<void> {
  if (!blockedAPI.value) {
    // Only allow one request add a time
    blockedAPI.value = true;
    // Get formated Timestamp
    let stamp = createTimestamp();
    let question = message.value;
    let msg: DeepshoreChatMessage = {
      id: chat.value.length,
      name: 'Du',
      text: question,
      stamp: stamp,
      //avatar: 'avatar.png',
      sent: true,
      textHtml: false
    };
    chat.value.push(msg);
    // Add tmp answer to chat
    let chatAnswer: DeepshoreChatMessage = {
      id: chat.value.length,
      name: 'Deepshore',
      text: '',
      stamp: stamp,
      avatar: '/user/themes/deepshore/images/deepshore.png',
      sent: false,
      textHtml: true
    };
    // Add "typing" answer to chat
    chat.value.push(chatAnswer);
    // Clear Input
    message.value = '';

    // Send question to backend
    let body: DeepshoreChatRequest = {
      question: question
    };
    const response = await sendQuestion(body);
    let answer: string;
    if (response.error) {
      answer = errMessages[getRandomInt(errMessages.length - 1)];
    } else {
      answer = buildAnswerText(response);
    }
    // Update Answer
    chat.value[chat.value.length - 1].text = answer;
    // Allow more requests
    blockedAPI.value = false;
  }

  /**
   * Build a bot chat answer containing answer text and article links as html containing string and return whole string.
   * @param response An axios response object of type DeepshoreChatResponse.
   */
  function buildAnswerText(response: DeepshoreChatResponse): string {
    let answer = response.answer;
    let articles = response.related_articles;
    let articleText = buildArticleText(articles);
    return `${answer}${articleText}`;
  }

  /**
   * Build a readable text for further articles using the specified articles array and return it as an string.
   * @param articles An array of article urls as strings.
   */
  function buildArticleText(articles: string[]): string {
    if (articles.length == 0 || articles == undefined) {
      return '';
    }
    // Start of additional article answer part
    let articleText = '</br></br>Weiterführende Artikel:<ul>';
    for (let article of articles) {
      // Get display name for article links if format: 'https://deepshore.de/knowledge/chatgpt-nlp'
      let articleNames = article.split('/');
      let articleName = articleNames[articleNames.length - 1];
      // Concate links as <a> tag list entries
      articleText = `${articleText}<li><a href="${article}" target="_blank">${articleName}</li>`;
    }
    // Close unsorted list
    articleText = `${articleText}</ul>`;
    return articleText;
  }

  /**
   * Create a timestamp for chat messages by specified format and return string of format 'HH:mm Uhr'.
   * @param format A valid date.formatDate format (default: 'HH:mm')
   */
  function createTimestamp(format = 'HH:mm'): string {
    const timeStamp = Date.now();
    const formattedString = `${date.formatDate(timeStamp, format)} Uhr`;
    return formattedString;
  }

  /**
   * Get a random number between 0 and max.
   * @param max A Integer
   */
  function getRandomInt(max: number): number {
    return Math.floor(Math.random() * max);
  }
}
</script>
