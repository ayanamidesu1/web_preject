import { defineStore } from 'pinia'

export const useCommentStore = defineStore('comment', {
    state: () => ({
        main_reply:null,
        comment_index:null,
        //评论区全局消息
        comment_global_msg:null,
        main_comment_info:{
            total:0,
            offset:0,
            limit:3,
        }
    }),
    actions: {
        debug(){
            console.log(this.$state)
        },
        set_main_reply(reply: any){
            this.main_reply = reply
        },
        set_comment_index (index:any) {
            this.$state.comment_index = index;
            console.log(this.$state.comment_index)
        },
        set_comment_global_msg(msg:any){
            this.comment_global_msg = msg
        },
        set_main_comment_info(total:number,offset:number=0,limit:number=3){
            this.main_comment_info.total = total
            this.main_comment_info.offset = offset
            this.main_comment_info.limit = limit
        }
    }
})