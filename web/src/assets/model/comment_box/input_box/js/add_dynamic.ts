async function add_dynamic(img_file_list:FileList,title:any,content:any) {
    try{
        let file=new FormData();
        for (let i = 0; i < img_file_list.length; i++) {
            file.append('img_file', img_file_list[i]);
        }
        file.append('title',title)
        file.append('content',content)
        const response = await fetch('http://localhost:8000/api/user/AddDynamic/',{
            method:'post',
            headers:{
                'Authorization':'Bearer '+localStorage.getItem('auth_token'),
            },
            body:file
        })
        if(response.ok)
        {
            const data=await response.json()
            return data
        }
        else{
            const data=await response.json()
            console.warn(data.msg)
            return data
        }
    }
    catch(e)
    {
        console.log(e)
    }
}

export default add_dynamic