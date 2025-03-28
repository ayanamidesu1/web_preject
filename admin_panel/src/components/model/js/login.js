async function admin_login(jwtToken=10086, userid = 10086, password = 10086) {
    try {
        const res = await fetch('https://www.sunyuanling.com/api/admin_control/AdminLogin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 将 JWT Token 放在 Authorization 头部
                'Authorization': `token ${jwtToken||''}`
            },
            credentials: 'include', // 确保 cookies 被包含在请求中
            body: JSON.stringify({
                userid: userid,
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
