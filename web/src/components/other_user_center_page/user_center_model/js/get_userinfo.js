async function get_userinfo(token=null,userid=null) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetAllUserInfo/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                'token': token,
                'userid':userid
            })
        })
        if (res.ok) {
            const data = await res.json()
            if (data.status == 'success') {
                return data.data
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
export {get_userinfo}