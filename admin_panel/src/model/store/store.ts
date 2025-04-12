import {defineStore} from 'pinia';

export const useStore = defineStore('main',{
    state:()=>({
        user:{},
        target_user:{},
        //wss连接
        ws:undefined,
        ws_ready:false,
    }),
    actions:{

    },
    getters:{

    }
})