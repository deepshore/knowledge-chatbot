<template>
  <div class="row justify-center" style="width: 66%">
    <div
      style="
        width: 100%;
        max-height: 85vh;
        min-height: 85vh;
        overflow-x: auto;
        padding: 1em;
      "
    >
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
    <div class="" style="width: 50%">
      <q-input
        outlined
        v-model="message"
        placeholder="Nachricht"
        @keyup.enter="addMessage"
      >
        <template v-slot:after>
          <q-btn
            title="Nachricht abschicken"
            color="secondary"
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
import {
  DeepshoreChatRequest,
  DeepshoreChatResponse,
  sendQuestion
} from '../api/index';

import { ChatMessage } from './models';

let message = ref('');
let chat: Ref<Array<ChatMessage>> = ref([]);
let blockedAPI = ref(false);
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

async function addMessage() {
  if (!blockedAPI.value) {
    // Only allow one request add a time
    blockedAPI.value = true;
    // Get formated Timestamp
    let stamp = createTimestamp();
    let question = message.value;
    let msg: ChatMessage = {
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
    let chatAnswer: ChatMessage = {
      id: chat.value.length,
      name: 'Deepshore',
      text: '',
      stamp: stamp,
      avatar: 'deepshore.png',
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
      answer =
        'Ich habe die Frage leider nicht verstanden. Bitte versuche es mit einer anderen Formulierung.';
    } else {
      answer = buildAnswerText(response);
    }
    // Update Answer
    chat.value[chat.value.length - 1].text = answer;
    // Allow more requests
    blockedAPI.value = false;
  }

  function buildAnswerText(response: DeepshoreChatResponse) {
    let answer = response.answer;
    let articles = response.related_articles;
    let articleText = buildArticleText(articles);
    return `${answer}${articleText}`;
  }

  function buildArticleText(articles: string[]) {
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

  function createTimestamp(format = 'HH:mm') {
    const timeStamp = Date.now();
    const formattedString = `${date.formatDate(timeStamp, format)} Uhr`;
    return formattedString;
  }
}
</script>
