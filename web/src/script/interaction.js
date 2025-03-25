async function watch_work(work_id,a_token,work_type,work_name) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/work_interaction/Watch/', {
            method: 'post',
            headers: {
                'Content-type': 'application/json'
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
                console.log(data.message)
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
export  {watch_work};