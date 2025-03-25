async function get_ill_workinfo(work_id){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/get_work_info/GetIllInfo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                work_id:work_id
            })
        })
        const data=await res.json();
        return data;
    }
    catch(err){
        console.log(err);
    }
}
async function get_comic_workinfo(work_id)
{
    try{
        const res=await fetch('https://www.sunyuanling.com/api/get_work_info/GetComicinfo/',{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                work_id:work_id
            })
        })
        const data=await res.json();
        return data;
    }
    catch(err){
        console.log(err);
    }
}
export { get_ill_workinfo,get_comic_workinfo}