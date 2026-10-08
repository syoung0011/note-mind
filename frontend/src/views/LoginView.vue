<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { login } from '@/services/auth'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
  if (isSubmitting.value) return
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await login(username.value, password.value)
    await router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = error instanceof TypeError
      ? '无法连接登录服务，请检查网络或稍后重试'
      : error.message || '登录失败，请稍后重试'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="page-card">
    <h1>登录 NoteMind</h1>

    <p v-if="route.query.reason === 'expired'" role="status">
      登录状态已失效，请重新登录。
    </p>

    <p v-if="route.query.reason === 'unavailable'" role="status">
      暂时无法确认登录状态，请检查网络后刷新页面，或重新登录。
    </p>

    <p v-if="route.query.registered === '1'" role="status">
      注册成功，请使用新账号登录。
    </p>

    <form class="login-form" @submit.prevent="handleSubmit">
      <label for="username">用户名</label>
      <input
        minlength="3"
        maxlength="50"
        id="username"
        v-model.trim="username"
        name="username"
        autocomplete="username"
        :disabled="isSubmitting"
        required
      />

      <label for="password">密码</label>
      <input
        minlength="8"
        maxlength="128"
        id="password"
        v-model="password"
        name="password"
        type="password"
        autocomplete="current-password"
        :disabled="isSubmitting"
        required
      />

      <p v-if="errorMessage" class="error-message" role="alert">
        {{ errorMessage }}
      </p>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? '正在登录…' : '登录' }}
      </button>
    </form>
    <p class="register-link">
      还没有账号？<RouterLink :to="{ name: 'register' }">创建账号</RouterLink>
    </p>
  </main>
</template>

<style scoped>
h1 {
  margin-bottom: 1.5rem;
}

.login-form {
  display: grid;
  gap: 0.75rem;
}

button {
  margin-top: 0.5rem;
}

.register-link {
  margin-top: 1rem;
}
</style>
