async function watch_work(work_id,a_token,work_type,work_name) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/work_interaction/Watch/', {
            method: 'post',
            headers: {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify({
                token: a_token,
                work_id: work_id,
                work_type: work_type,
                work_name: work_name,
            })
        })
        if (res.ok) {
            const data = await res.json()
            if (data.status == 'success') {
                return data.count;
            }
            else {
                console.log(data.message)
            }
        }
        else {
            console.log(res.status)
        }
    }
    catch (e) {
        console.log(e)
    }
}
//作品点赞
async function like_work(work_id, operate_type, token, work_type, work_name) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/work_interaction/Like/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify({
                work_id: work_id,
                operate_type: operate_type,
                token: token,
                work_type: work_type,
                work_name: work_name,
            })
        })
        if (res.ok) {
            const data =await res.json()
            if (data.status == 'success') {
                return data.data;
            }
            else{
                console.log(data.message)
                return data.data;
            }
        }
        else{
            console.log(res.status)
        }
    }
    catch (e) {
        console.log(e)
    }
}
async function collect_work(work_id, operate_type, token, work_type, work_name) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/work_interaction/Collect/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify({
                work_id: work_id,
                operate_type: operate_type,
                token: token,
                work_type: work_type,
                work_name: work_name,
            })
        })
        if (res.ok) {
            const data =await res.json()
            if (data.status == 'success') {
                return data.data;
            }
            else{
                console.log(data.message)
                return data.data;
            }
        }
        else{
            console.log(res.status)
        }
    }
    catch (e) {
        console.log(e)
    }
}
export  {watch_work,like_work,collect_work};