async function update_user_back(file, token, user_data) {
    let formdata = new FormData();
    formdata.append('files', file);
    formdata.append('data', JSON.stringify(user_data));
    formdata.append('token', token);

    try {
        const res = await fetch('https://www.sunyuanling.com/api/update/UpdateUserBack/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: formdata
        });

        // Check for HTTP errors
        if (!res.ok) {
            console.error('HTTP error:', res.status, res.statusText);
            const data = await res.json();
            if (data.status === 'file_error') {
                alert(data.message);
                console.log(data.message);
                alert('上传失败，请重试');
                return false;
            }
            return false;
        }

        // Parse JSON response
        const data = await res.json();

        // Check for response status
        if (data.status === 'success') {
            return true;
        } else if (data.status === 'file_error') {
            alert(data.message);
            console.log(data.message);
            alert('上传失败，请重试');
            return false;
        } else {
            console.error('Upload failed:', data.message);
            return false;
        }
    } catch (e) {
        // Handle unexpected errors
        console.error('Error:', e);
        return false;
    }
}


async function delete_user_back(token) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/update/DeleteUserBack/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                token: token
            })
        });

        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                return true;
            } else {
                console.error('Upload failed:', data.message);
                return false;
            }
        }
    }
    catch (e) {
        console.error('Error:', e);
    }
}

async function update_userinfo(token, userinfo, files) {
    let formdata = new FormData();
    formdata.append('token', token);
    formdata.append('files', files);
    console.log(files)
    formdata.append('data', userinfo);
    console.log(formdata)
    try {
        const res = await fetch('https://www.sunyuanling.com/api/update/UpdateUserInfo/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: formdata
        })
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                alert(data.message);
                return true;
            }
            else {
                console.log(data.message);
                return false;
            }
        }
        else {
            const data = await res.json();
            if (data.status === 'file_error') {
                alert(data.message);
                return false;
            }
        }
    }
    catch (e) {
        console.log(e);
    }
}
async function update_user_select_work(token, select_work) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/update/UpdateUserSelectWork/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                select_work: select_work,
                token: token
            })
        })
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'success') {
                return true;
            }
            else {
                return '更新失败';
            }
        }
        else {
            return '更新失败';
        }
    }
    catch (e) {
        console.log(e);
    }
}

async function update_user_collect_work(token, collect_id, work_type, operate, open_operate) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/update/UpdateUserCollect/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                body: JSON.stringify({
                    'token': token,
                    'collect_id': collect_id,
                    'work_type': work_type,
                    'operate': operate,
                    'open_operate': open_operate
                })
            }
        )
        if (res.ok) {
            const data =await res.json()
            if (data.status == 'success') {
                console.log(data.message);
                return true;
            }
            else {
                console.log(data.message);
                return false;
            }
        }
        else {
            console.log(res.status);
            const data =await res.json()
            return data.message;
        }
    }
    catch (e) {
        console.log(e);
    }
}
export { update_user_back, delete_user_back, update_userinfo, update_user_select_work ,update_user_collect_work};
