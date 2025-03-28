import { defineStore } from "pinia";

export const useChatStore = defineStore("chat", {
    state: () => ({
       now_chat_user:null,
       //聊天wss连接
       ws:null,
    }),
})