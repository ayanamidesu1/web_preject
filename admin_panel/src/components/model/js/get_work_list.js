async function get_ill_worklist(limit = 10, offset = 0) {
    try {
        const res = await fetch("https://www.sunyuanling.com/api/admin_control/GetIllList/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
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
async function get_comic_worklist(limit = 10, offset = 0) {
    try {
        const res = await fetch("https://www.sunyuanling.com/api/admin_control/GetComicList/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
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

async function get_novel_work_list(limit = 10, offset = 0) {
    try {
        const res = await fetch("https://www.sunyuanling.com/api/admin_control/GetNovelWork/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
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

async function get_novel_work_content_list(work_id, limit = 10, offset = 0) {
    try {
        const res = await fetch("https://www.sunyuanling.com/api/admin_control/GetNovelContentList/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                work_id: work_id,
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

async function get_comment_list(limit = 10, offset = 0) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/GetCommentList/', {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                limit: limit,
                offset: offset
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

export { get_ill_worklist, get_comic_worklist, get_novel_work_list, get_novel_work_content_list,get_comment_list }