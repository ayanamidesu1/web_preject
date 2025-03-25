async function get_workinfo(token, work_list) {
    const server_url = 'https://www.sunyuanling.com/api/get_work_info/';
    
    try {
        // 循环处理每个工作
        for (let i = 0; i < work_list.length; i++) {
            const work = work_list[i];
            const workType = work.work_type;
            const workId = work.work_id;

            try {
                // 定义请求配置
                const requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        token: token,
                        work_id: workId
                    })
                };

                // 选择相应的接口
                let endpoint;
                switch (workType) {
                    case 'ill':
                        endpoint = 'GetIllInfo/';
                        break;
                    case 'comic':
                        endpoint = 'GetComicinfo/';
                        break;
                    case 'novel':
                        endpoint = 'GetNovelInfo/';
                        break;
                    default:
                        console.error(`未知的工作类型: ${workType}`);
                        continue;
                }

                // 发送请求
                const res = await fetch(server_url + endpoint, requestOptions);

                if (res.ok) {
                    const data = await res.json();
                    if (data.status === 'success') {
                        work.work_info = data.data;
                    } else {
                        console.error(`获取工作信息失败: ${data.message}`);
                    }
                } else {
                    console.error(`请求失败: ${res.status} ${res.statusText}`);
                }
            } catch (e) {
                console.error(`处理 ${workType} 类型工作时出错:`, e);
            }
        }

        // 返回更新后的 work_list
        return work_list;
    } catch (err) {
        console.error('获取工作信息时发生错误:', err);
        throw err;  // 可以重新抛出错误以供调用方处理
    }
}

async function get_user_all_worklist(token)
{
    try{
        const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserWorkList/',
            {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                body:JSON.stringify({
                    token:token
                })
            }
        )
        if(res.ok)
        {
            const data=await res.json();
            if (data.status==='success'){
                return data.data;
            }
            else{
                return data.message;
            }
        }
        else{
            console.log('Error:',res.status);
        }
    }
    catch(e)
    {
        console.error('获取工作信息时发生错误:', e);
    }
}
async function get_user_collect_worklist(token){
    try{
        const res=await fetch('https://www.sunyuanling.com/api/GetUserInfo/GetUserCollect/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body:JSON.stringify({
                token:token
            })
        })
        if (res.ok)
        {
            const data=await res.json();
            if (data.status==='success'){
                return data.data;
            }
            else{
                return data.message;
            }
        }
        else{
            console.log('Error:',res.status);
        }
    }
    catch(e)
    {
        console.log(e)
    }
}
export{get_workinfo,get_user_all_worklist,get_user_collect_worklist}