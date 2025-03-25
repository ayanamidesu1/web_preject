async function search_ill_work(search_key="", work_status="all") {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/SearchIllWork/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',  // 修正为 'Content-Type'
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_key: search_key,
                work_status: work_status
            })
        });
        const data = await res.json();
        return data;
    } catch (e) {
        console.log(e);
    }
}

async function search_comic_work(search_key="", work_status="all") {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/SearchComicWork/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',  // 修正为 'Content-Type'
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_key: search_key,
                work_status: work_status
            })
        });
        const data = await res.json();
        return data;
    } catch (e) {
        console.log(e);
    }
}

async function search_novel_work(search_key="", work_status="all") {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/get_work_info/SearchNovelWork/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',  // 修正为 'Content-Type'
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                search_key: search_key,
                work_status: work_status
            })
        });
        const data = await res.json();
        return data;
    } catch (e) {
        console.log(e);
    }
}

export { search_ill_work, search_comic_work, search_novel_work }
