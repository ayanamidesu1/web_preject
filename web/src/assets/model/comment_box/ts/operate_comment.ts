import base_api from "./base_api";

async function add_comment(comment:any) {
    try{
        const res=await base_api.post('api/work_interaction/AddComment',{
            content:comment.content,
            is_main:comment.is_main,
            reply_comment_id:comment.reply_comment_id,
            reply_work_id:comment.reply_work_id,
            reply_work_type:comment.reply_work_type,
            reply_user_id:comment.reply_user_id,
        })
        return res
    }
    catch(err){
        console.log(err);
    }
}
async function get_comment(work_id:any,work_type:any,limit:any,offset:any,reply_limit:any,reply_offset:any){
    try{
        const res=await base_api.post('api/work_interaction/GetCommentList',{
            work_id:work_id,
            work_type:work_type,
            limit:limit,
            offset:offset,
            reply_limit:reply_limit,
            reply_offset:reply_offset,
        })
        console.log(res);
        return res
    }
    catch(e)
    {
        console.log(e);
    }
}

//获取更多主评论
async function get_more_main_comment(work_id:any,work_type:any,limit:any,offset:any){
    try{
        const res=await base_api.post('api/work_interaction/GetMoreMainComment',{
            work_id:work_id,
            work_type:work_type,
            limit:limit,
            offset:offset,
        })
        return res
    }
    catch(e)
    {
        console.log(e);
    }
}

//获取更多回复
async function get_more_reply(comment_id:any,limit:any,offset:any){
    try{
        const res=await base_api.post('api/work_interaction/GetMoreReplyComment',{
            comment_id:comment_id,
            limit:limit,
            offset:offset,
        })
        return res
    }
    catch(e)
    {
        console.log(e);
    }
}
async function like_comment(comment_id:any) {
    try{
        const res=await base_api.post('api/work_interaction/LikeComment/',{
            comment_id:comment_id,
        })
        return res
    }
    catch(e){
        console.log(e);
    }
}
export {add_comment,get_comment,get_more_main_comment,get_more_reply,like_comment}