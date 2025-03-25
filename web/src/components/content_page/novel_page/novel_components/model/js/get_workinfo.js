async function get_workinfo(token,work_id)
{
    try{
        const res=await fetch('https://www.sunyuanling.com/api/get_work_info/GetNovelList/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body:JSON.stringify({
                token:token,
                work_id:work_id
            })
        })
        if(res.ok)
        {
            const data=await res.json()
            if(data.status=='success')
            {
                return data.data
            }
            else
            {
                console.log(data.message)
            }
        }
        else
        {
            console.log('请求失败')
        }
    }
    catch(e)
    {
        console.log(e)
    }
}
async function get_novel_content(token,work_id,title)
{
    try{
        const res=await fetch('https://www.sunyuanling.com/api/get_work_info/GetNovelContent/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body:JSON.stringify({
                token:token,
                work_id:work_id,
                title:title
            })
        })
        if(res.ok)
        {
            const data=await res.json()
            if (data.status=='success')
            {
                return data.data
            }
            else
            {
                console.log(data.message)
            }
        }
        else{
            console.log(res.status)
        }
    }
    catch(e)
    {
        console.log(e)
    }
}
export {get_workinfo,get_novel_content}