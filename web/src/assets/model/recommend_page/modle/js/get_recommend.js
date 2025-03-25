async function get_recommend(token,work_type,work_offset,work_limit)
{
    try{
        const res=await fetch('https://www.sunyuanling.com/api/recommend/recommentd/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                token:token,
                work_type:work_type,
                work_offset:work_offset,
                work_limit:work_limit
            })
        })
        if(res.ok)
        {
            const data=await res.json();
            if (data.status=='success')
            {
                return data.data;
            }
            else{
                return data.message;
            }
        }
        else{
            return res.status;
        }
    }
    catch(e)
    {
        console.log(e);
    }
}

export {get_recommend};