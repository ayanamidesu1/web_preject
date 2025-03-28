async function edit_userinfo({
    userid = null,
    username = null,
    user_avatar = null,
    user_address = null,
    password = null,
    user_back_img = null,
    phone = null,
    email = null,
    user_self_website = null,
    sex = null,
    select_work = null,
    occupation = null,
    birthday = null,
    vip = null,
    account_status = null,
    account_permissions = null
} = {}) {
    try {
        const res = await fetch("https://www.sunyuanling.com/api/admin_control/EditUserInfo/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "token " + localStorage.getItem("token"),
            },
            credentials: "include",
            body: JSON.stringify({
                userid,
                username,
                user_avatar,
                user_address,
                password,
                user_back_img,
                phone,
                email,
                user_self_website,
                sex,
                select_work,
                occupation,
                birthday,
                vip,
                account_status,
                account_permissions
            })
        });

        const data = await res.json();

        if (res.ok) {
            console.log("修改成功:", data);
            return data;
        } else {
            console.error("修改失败:", data);
            return data;
        }
    } catch (e) {
        console.log("请求发生错误:", e);
    }
}

export { edit_userinfo };