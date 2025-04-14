<template>
    <div class="submit-work">
        <h2 class="submit-work__title">提交完成的作品</h2>

        <div class="submit-work__input">
            <input type="file" @change="onFileChange" accept=".png,.jpg,.jpeg,.gif,.webp,.bmp,.psd,.zip,.rar,.7z" />
        </div>

        <button @click="submitWork" :disabled="isSubmitting" class="submit-work__button">
            {{ isSubmitting ? '提交中...' : '提交' }}
        </button>

        <p v-if="message" class="submit-work__message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const file = ref(null)
const isSubmitting = ref(false)
const message = ref('')
const router = useRouter()

function onFileChange(event) {
    file.value = event.target.files[0]
}

async function submitWork() {
    const orderId = router.currentRoute.value.query.id
    const user_id=router.currentRoute.value.query.user_id
    const token = localStorage.getItem('token')

    if (!token) {
        message.value = '未登录，缺少令牌'
        return
    }

    if (!orderId) {
        message.value = '缺少订单ID'
        return
    }

    if (!file.value) {
        message.value = '请先选择要提交的文件'
        return
    }

    isSubmitting.value = true
    message.value = ''

    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('data', JSON.stringify({ order_id: orderId,target_user_id:user_id }))

    try {
        const response = await fetch('https://www.sunyuanling.com/api/api/CompleteWork', {
            method: 'POST',
            headers: {
                Authorization: `token ${token}`
            },
            body: formData,
        })

        const result = await response.json()

        if (response.ok && result.code === 200) {
            message.value = '✅ 提交成功'
            console.log(response)
        } else {
            message.value = result.msg || '❌ 提交失败'
            console.log(response)
        }
    } catch (error) {
        console.error('提交失败', error)
        message.value = '服务器异常，请稍后重试'
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped lang="scss">
.submit-work {
    max-width: 420px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    align-items: stretch;

    &__title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d2d2d;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    &__input {
        margin-bottom: 1.25rem;

        input[type='file'] {
            display: block;
            width: 100%;
            padding: 0.5rem;
            font-size: 0.95rem;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f9f9f9;
            cursor: pointer;

            &:hover {
                background-color: #f0f0f0;
            }
        }
    }

    &__button {
        padding: 0.6rem;
        background-color: #2563eb;
        color: #ffffff;
        font-size: 1rem;
        font-weight: 500;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
            background-color: #1d4ed8;
        }

        &:disabled {
            background-color: #93c5fd;
            cursor: not-allowed;
        }
    }

    &__message {
        margin-top: 1rem;
        text-align: center;
        font-size: 0.9rem;
        color: #444;
    }
}
</style>