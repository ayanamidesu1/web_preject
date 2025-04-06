async function admin_login(jwtToken=10086, userid = 10086, password = 10086) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                login_key: userid,
                password: password,
                login_type:'back_end'
            })
        });

        // 处理响应
        if (res.ok) {
            const data = await res.json();
            return data;
        } else {
            const data = await res.json();
            return data;
        }
    } catch (e) {
        console.log(e);
    }
}

export { admin_login };
