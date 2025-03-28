async function get_user_list(offset=0,limit=10){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/admin_control/GetUserList/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`token ${localStorage.getItem('token')}`
            },
            credentials:'include',
            body:JSON.stringify({
                offset:offset,
                limit:limit
            })
        })
        if (res.ok)
        {
            const data=await res.json();
            console.log(data);
            return data;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}
export {get_user_list};