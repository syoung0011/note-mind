<script setup>
import { onMounted, ref } from 'vue'

const title = 'NoteMind'
const description = '基于个人笔记进行检索与问答'
const backendStatus = ref('正在连接后端…')
const connectionState = ref('loading')

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/health')

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()

    if (data.status !== 'ok') {
      throw new Error('后端返回了未知状态')
    }

    backendStatus.value = '后端连接正常'
    connectionState.value = 'success'
  } catch (error) {
    backendStatus.value = '后端连接失败'
    connectionState.value = 'error'
    console.error('连接 NoteMind API 失败：', error)
  }
})
</script>

<template>
  <main class="home-page">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <p class="status" :class="connectionState">{{ backendStatus }}</p>
  </main>
</template>

<style scoped>
.home-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 4rem 1.5rem;
  text-align: center;
}

.home-page h1 {
  margin-bottom: 1rem;
  color: #2563eb;
}

.status {
  margin-top: 1.5rem;
}

.loading {
  color: #475569;
}

.success {
  color: #15803d;
}

.error {
  color: #b91c1c;
}
</style>
