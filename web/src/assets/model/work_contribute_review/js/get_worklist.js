async function get_worklist(offset = 0, limit = 3) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkList/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                body: JSON.stringify({
                    offset: offset,
                    limit: limit
                })
            }
        )
        const data = await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}

async function get_chapter_list(work_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/GetChapterList/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                work_id: work_id
            })
        })
        const data = await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}
async function get_novel_info(work_id) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/GetNovelInfo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },

            body: JSON.stringify({
                work_id: work_id

            })
        })
        const data = await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}
export { get_worklist, get_chapter_list ,get_novel_info}