<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { register } from '@/services/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

function passwordsMatch() {
  return password.value === confirmPassword.value
}

async function handleSubmit() {
  if (isSubmitting.value) return
  errorMessage.value = ''

  if (!passwordsMatch()) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  isSubmitting.value = true
  try {
    await register(username.value.trim().toLowerCase(), password.value)
    password.value = ''
    confirmPassword.value = ''
    await router.push({ name: 'login', query: { registered: '1' } })
  } catch (error) {
    errorMessage.value = error instanceof TypeError
      ? '无法连接注册服务，请检查网络或稍后重试'
      : error.message || '注册失败，请稍后重试'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="page-card">
    <h1>注册 NoteMind</h1>
    <p class="intro">创建账号，开始整理你的学习笔记。</p>

    <form class="register-form" @submit.prevent="handleSubmit">
      <label for="register-username">用户名</label>
      <input
        id="register-username"
        v-model.trim="username"
        name="username"
        autocomplete="username"
        minlength="3"
        maxlength="50"
        pattern="[A-Za-z0-9_]+"
        aria-describedby="username-help"
        :disabled="isSubmitting"
        required
      />
      <small id="username-help">3～50 个字母、数字或下划线；大写字母会转为小写。</small>

      <label for="register-password">密码</label>
      <input
        id="register-password"
        v-model="password"
        name="password"
        type="password"
        autocomplete="new-password"
        minlength="8"
        maxlength="128"
        aria-describedby="password-help"
        :disabled="isSubmitting"
        required
      />
      <small id="password-help">8～128 个字符，请勿使用其他网站的重要密码。</small>

      <label for="register-confirm-password">确认密码</label>
      <input
        id="register-confirm-password"
        v-model="confirmPassword"
        name="confirmPassword"
        type="password"
        autocomplete="new-password"
        minlength="8"
        maxlength="128"
        :disabled="isSubmitting"
        required
      />

      <p v-if="errorMessage" class="error-message" role="alert">{{ errorMessage }}</p>
      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? '正在注册…' : '创建账号' }}
      </button>
    </form>

    <p class="login-link">已有账号？<RouterLink :to="{ name: 'login' }">去登录</RouterLink></p>
  </main>
</template>

<style scoped>
.intro {
  margin: 0.75rem 0 1.5rem;
}

.register-form {
  display: grid;
  gap: 0.75rem;
}

small {
  color: var(--color-muted);
}

button,
.login-link {
  margin-top: 0.75rem;
}
</style>
