class BaseApi {
    private ip: string = 'https://www.sunyuanling.com/';
    private token: string | null = localStorage.getItem('token');

    // POST 请求方法
    public async post<T>(url: string, body: Object): Promise<T> {
        try {
            // 准备请求头
            const headers: HeadersInit = {
                'Content-Type': 'application/json',
            };

            if (this.token) {
                headers['Authorization'] = `token ${this.token}`;
            }

            // 发送请求
            const response = await fetch(this.ip + url, {
                method: 'POST',
                headers,
                body: JSON.stringify(body),
            });

            // 检查响应状态
            if (!response.ok) {
                throw new Error(`请求失败，状态码: ${response.status}`);
            }

            // 解析响应数据
            const data: T = await response.json();
            console.log(data);
            return data;
        } catch (error) {
            // 错误处理
            console.error('请求错误:', error);
            throw error; // 可以在调用时捕获并处理
        }
    }
}

export default new BaseApi();
