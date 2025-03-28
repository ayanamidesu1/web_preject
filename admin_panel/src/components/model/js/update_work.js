async function update_ill_work_status(work_status, work_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/UpdateIll/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                work_status: work_status,
                work_id: work_id
            })
        })
        const data = await res.json();
        return data;
    }
    catch (e) {
        console.log(e);
    }
}

async function update_comic_work_status(work_status, work_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/UpdateComic/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                work_status: work_status,
                work_id: work_id
            })
        })
        const data = await res.json();
        return data;
    }
    catch (e) {
        console.log(e);
    }
}

async function update_novel_work_status(work_status, work_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/UpdateNovelWork/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                work_status: work_status,
                work_id: work_id
            }
            )
        })
        const data = await res.json();
        return data;
    }
    catch (e) {
        console.log(e);
    }
}

async function update_novel_chapter_status(work_status, work_id,chapter_id) {
    try{
        let res=await fetch('https://www.sunyuanling.com/api/admin_control/UpdateNovelContent/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'token '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                work_status:work_status,
                work_id:work_id,
                chapter_id:chapter_id
            })
        })
        let data=await res.json();
        return data;
    }
    catch(e)
    {
        console.log(e);
    }
}

async function delete_comment(comment_id_list) {
    try{
        const res=await fetch('https://www.sunyuanling.com/api/admin_control/DeleteComment/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'token '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                comment_id_list:comment_id_list
            })
        })
        const data=await res.json();
        return data;
    }
    catch(e)
    {
        console.log(e);
    }
}
async function update_comment(comment_id,content){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/admin_control/UpdateComment/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'token '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                comment_id:comment_id,
                content:content
            })
        })
        const data=await res.json();
        return data;
    }
    catch(e)
    {
        console.log(e);
    }
}

export { update_ill_work_status, update_comic_work_status ,update_novel_work_status,update_novel_chapter_status,
    delete_comment, update_comment
};