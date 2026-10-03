<script setup>
const title = 'NoteMind'
const description = '基于个人笔记进行检索与问答'
const status = '前端已启动'
</script>

<template>
  <main class="home-page">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <p class="status">{{ status }}</p>
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
  color: #15803d;
}
</style>
