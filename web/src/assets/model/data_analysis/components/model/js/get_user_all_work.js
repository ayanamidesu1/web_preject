async function get_all_user_work(token){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkList/',{
            method:'post',
            headers:{
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                token:token
            })
        })
        if(res.ok)
        {
            const data=await res.json()
            if(data.status=='success')
            {
                return data.data
            }
            else{
                return data.message
            }
        }
        else{
            return '网络错误'
        }
    }
    catch(e)
    {
        console.log(e)
    }
}

export {get_all_user_work}