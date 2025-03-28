async function search_ill_work(search_key, work_status = 'all', limit = 10, offset = 0) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/SearchIll/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_key: search_key,
                work_status: work_status,
                limit: limit,
                offset: offset
            })
        })
        const data = await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}

async function search_comic_work(search_key, work_status = 'all', limit = 10, offset = 0) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/SearchComic/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_key: search_key,
                work_status: work_status,
                limit: limit,
                offset: offset
            })
        })
        const data = await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}

async function search_novel_work(search_key, work_status = 'all', limit = 10, offset = 0) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/SearchNovelWork/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_type: search_key,
                work_status: work_status,
                limit: limit,
                offset: offset
            })
        })
        const data = await res.json()
        return data;
    }
    catch (e) { console.log(e) }
}

async function search_comment(limit=10,offset=0,comment_id=null,work_id=null,work_type=null,
    send_userid=null,main_userid=null,accuracy_type='vague')
{
 try{
        const res=await fetch('https://www.sunyuanling.com/api/admin_control/SearchComment/',{
            method:'post',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('token')
            },
            body:JSON.stringify({
                limit:limit,
                offset:offset,
                comment_id:comment_id,
                work_id:work_id,
                work_type:work_type,
                send_userid:send_userid,
                main_userid:main_userid,
                accuracy_type:accuracy_type
            })
        })
        const data=await res.json()
        return data
 }
 catch(e)
 {
    console.log(e)
 }
}

export { search_ill_work, search_comic_work,search_novel_work ,search_comment}