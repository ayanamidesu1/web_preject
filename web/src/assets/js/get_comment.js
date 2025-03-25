async function get_comment(work_id,work_type,token,limit=5,offset=0){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/work_interaction/GetCommentSection/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body:JSON.stringify({
                work_id:work_id,
                work_type:work_type,
                token:token,
                limit:limit,
                offset:offset
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            if(data.status=='success')
            {
                return data.data;
            }
            else
            {
                console.log(data.message);
                return null;
            }
        }
        else
        {
            console.log('网络错误');
            return null;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}
async function add_comment(work_id,work_type,token,send_userid,is_root_comment,content,main_userid,main_comment_id,reply_comment_id){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/work_interaction/AddCommentSection/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body:JSON.stringify({
                work_id:work_id,
                work_type:work_type,
                token:token,
                send_userid:send_userid,
                is_root_comment:is_root_comment,
                content:content,
                main_userid:main_userid,
                main_comment_id:main_comment_id,
                reply_comment_id:reply_comment_id
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            if (data.status == 'success') {
                console.log(data.message);
                alert('评论可能有延迟，请刷新后查看')
            } else {
                console.log(data.message);
                return null;
            }
        }
        else if(res.status==400)
        {
            const data=await res.json();
            alert(data.message)
        }
    }
    catch(e)
    {
        console.log(e);
    }
}
async function like_comment(comment_id,operate,token,work_type,work_id){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/work_interaction/LikeComment/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body:JSON.stringify({
                comment_id:comment_id,
                operate:operate,
                token:token,
                work_type:work_type,
                work_id:work_id
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            if(data.status=='success')
            {
                console.log(data.message);
            }
            else
            {
                console.log(data.message);
                return null;
            }
        }
        else
        {
            console.log('网络错误');
            return null;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}
export {get_comment,add_comment,like_comment}