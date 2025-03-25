async function get_history(limit=100,offset=0) {
    try{
        const res=await fetch('https://www.sunyuanling.com/api/get_browse_history/GetHistory/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                'userid':'',
                'limit':limit,
                'offset':offset
            })
        })
        const data=await res.json()
        return data
    }
    catch (e) {
        console.log(e)
    }
}

export{get_history}