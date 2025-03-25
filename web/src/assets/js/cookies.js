// utils.js

// 设置cookies
async function set_cookie(key, value) {
    expireCookie(key);
    let now = new Date();
    now.setTime(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    let expires = "expires=" + now.toUTCString();
    let newCookie = key + '=' + value + '; ' + expires;
    let cookies = document.cookie;
    if (cookies.includes(key + '=')) {
        let cookieArray = cookies.split('; ');
        for (let i = 0; i < cookieArray.length; i++) {
            if (cookieArray[i].startsWith(key + '=')) {
                cookieArray[i] = newCookie;
            }
        }
        document.cookie = cookieArray.join('; ');
    } else {
        document.cookie = newCookie;
    }
}

function expireCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

// 获取指定cookie的值
function get_cookie(name) {
    let cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].split('=');
        if (cookie[0] === name) {
            return cookie[1];
        }
    }
    return null; // Cookie not found
}

// 设置localStorage值，设置前清除之前的值
function set_storage(key, value) {
    localStorage.removeItem(key);
    localStorage.setItem(key, value);
}

// 获取localStorage值
function get_storage(key) {
    return localStorage.getItem(key);
}

//清楚所有cookies
function clearAllCookies() {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }
}
//清除所有localStrong
function clearAllLocalStorage() {
    localStorage.clear();
}
//清除所有session
function clearAllSessionStorage() {
    sessionStorage.clear();
}

// 导出所有函数
export { set_cookie, expireCookie, get_cookie, set_storage, get_storage, clearAllCookies, clearAllLocalStorage, clearAllSessionStorage};
