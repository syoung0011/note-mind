<script setup>
import { RouterLink } from 'vue-router'

import { currentUser } from '@/services/auth'
</script>

<template>
  <div class="app-shell">
    <header class="app-shell__header">
      <div class="app-shell__bar">
        <RouterLink class="app-shell__brand" :to="{ name: 'home' }">
          NoteMind
        </RouterLink>
        <nav class="app-shell__nav" aria-label="主导航">
          <RouterLink v-if="currentUser" :to="{ name: 'home' }">
            我的笔记
          </RouterLink>
          <RouterLink v-else :to="{ name: 'login' }">登录</RouterLink>
        </nav>
        <span v-if="currentUser" class="app-shell__user">
          {{ currentUser.username }}
        </span>
      </div>
    </header>

    <div class="app-shell__content">
      <!-- 父组件放在 AppShell 标签之间的内容会渲染到这里。 -->
      <slot />
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-shell__header {
  border-bottom: 1px solid #dbe3ef;
  background: var(--color-surface);
  color: var(--color-text);
}

.app-shell__bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 1rem var(--space-page);
}

.app-shell__brand {
  color: var(--color-primary);
  font-size: 1.25rem;
  font-weight: 700;
  text-decoration: none;
}

.app-shell__nav a {
  color: inherit;
  text-decoration: none;
}

.app-shell__user {
  margin-left: auto;
  overflow-wrap: anywhere;
}

.app-shell__content {
  min-width: 0;
}
</style>
