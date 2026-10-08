<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { login } from '@/services/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await login(username.value, password.value)
    await router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="page-card">
    <h1>登录 NoteMind</h1>

    <form class="login-form" @submit.prevent="handleSubmit">
      <label for="username">用户名</label>
      <input
        minlength="3"
        maxlength="50"
        id="username"
        v-model="username"
        name="username"
        autocomplete="username"
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
        required
      />

      <p v-if="errorMessage" class="error-message" role="alert">
        {{ errorMessage }}
      </p>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? '正在登录…' : '登录' }}
      </button>
    </form>
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
</style>
