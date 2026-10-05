<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { currentUser, logout } from '@/services/auth'
import {
  createNote,
  deleteNote,
  getNote,
  listNotes,
  updateNote,
} from '@/services/notes'

const router = useRouter()
const notes = ref([])
const newTitle = ref('')
const newContent = ref('')
const selectedNote = ref(null)
const editTitle = ref('')
const editContent = ref('')
const isLoading = ref(true)
const isCreating = ref(false)
const isSaving = ref(false)
const isDeleting = ref(false)
const errorMessage = ref('')

async function loadNotes() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    notes.value = await listNotes()
  } catch (error) {
    await handleRequestError(error)
  } finally {
    isLoading.value = false
  }
}

async function handleCreate() {
  errorMessage.value = ''
  isCreating.value = true

  try {
    const createdNote = await createNote({
      title: newTitle.value,
      content: newContent.value,
    })
    notes.value.unshift(createdNote)
    newTitle.value = ''
    newContent.value = ''
  } catch (error) {
    await handleRequestError(error)
  } finally {
    isCreating.value = false
  }
}

async function selectNote(noteId) {
  errorMessage.value = ''

  try {
    const note = await getNote(noteId)
    selectedNote.value = note
    editTitle.value = note.title
    editContent.value = note.content
  } catch (error) {
    await handleRequestError(error)
  }
}

async function handleUpdate() {
  errorMessage.value = ''
  isSaving.value = true

  try {
    const updatedNote = await updateNote(selectedNote.value.id, {
      title: editTitle.value,
      content: editContent.value,
    })
    const noteIndex = notes.value.findIndex((note) => note.id === updatedNote.id)

    selectedNote.value = updatedNote
    if (noteIndex !== -1) {
      notes.value[noteIndex] = updatedNote
    }
  } catch (error) {
    await handleRequestError(error)
  } finally {
    isSaving.value = false
  }
}

async function handleDelete() {
  if (!window.confirm('确定要删除这篇笔记吗？此操作无法撤销。')) {
    return
  }

  const noteId = selectedNote.value.id
  errorMessage.value = ''
  isDeleting.value = true

  try {
    await deleteNote(noteId)
    notes.value = notes.value.filter((note) => note.id !== noteId)
    selectedNote.value = null
    editTitle.value = ''
    editContent.value = ''
  } catch (error) {
    await handleRequestError(error)
  } finally {
    isDeleting.value = false
  }
}

async function handleRequestError(error) {
  if (error.status === 401) {
    await handleLogout()
    return
  }

  errorMessage.value = error.message
}

async function handleLogout() {
  logout()
  await router.push({ name: 'login' })
}

onMounted(loadNotes)
</script>

<template>
  <main class="notes-page">
    <header class="page-header">
      <div>
        <p class="eyebrow">NoteMind</p>
        <h1>我的笔记</h1>
        <p v-if="currentUser">当前用户：{{ currentUser.username }}</p>
      </div>
      <button class="secondary-button" type="button" @click="handleLogout">
        退出登录
      </button>
    </header>

    <p v-if="errorMessage" class="error-message" role="alert">
      {{ errorMessage }}
    </p>

    <section class="notes-layout">
      <form class="panel create-form" @submit.prevent="handleCreate">
        <h2>创建笔记</h2>

        <label for="new-title">标题</label>
        <input id="new-title" v-model="newTitle" maxlength="200" required />

        <label for="new-content">正文</label>
        <textarea
          id="new-content"
          v-model="newContent"
          rows="10"
          required
        ></textarea>

        <button type="submit" :disabled="isCreating">
          {{ isCreating ? '正在创建…' : '创建笔记' }}
        </button>
      </form>

      <section class="panel notes-list" aria-live="polite">
        <h2>笔记列表（{{ notes.length }}）</h2>
        <p v-if="isLoading">正在加载笔记…</p>
        <p v-else-if="notes.length === 0">还没有笔记，请先创建一篇。</p>
        <button
          v-for="note in notes"
          v-else
          :key="note.id"
          class="note-card"
          type="button"
          @click="selectNote(note.id)"
        >
          <strong>{{ note.title }}</strong>
          <span>{{ note.content }}</span>
        </button>
      </section>
    </section>

    <form
      v-if="selectedNote"
      class="panel edit-form"
      @submit.prevent="handleUpdate"
    >
      <h2>编辑笔记</h2>

      <label for="edit-title">标题</label>
      <input id="edit-title" v-model="editTitle" maxlength="200" required />

      <label for="edit-content">正文</label>
      <textarea
        id="edit-content"
        v-model="editContent"
        rows="10"
        required
      ></textarea>

      <div class="form-actions">
        <button type="submit" :disabled="isSaving || isDeleting">
          {{ isSaving ? '正在保存…' : '保存修改' }}
        </button>
        <button
          class="danger-button"
          type="button"
          :disabled="isSaving || isDeleting"
          @click="handleDelete"
        >
          {{ isDeleting ? '正在删除…' : '删除笔记' }}
        </button>
      </div>
    </form>
  </main>
</template>

<style scoped>
.notes-page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-header h1,
.panel h2 {
  margin: 0 0 0.75rem;
}

.eyebrow {
  margin: 0 0 0.25rem;
  color: #2563eb;
  font-weight: 700;
}

.notes-layout {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 1.5rem;
}

.panel {
  border: 1px solid #dbe3ef;
  border-radius: 0.75rem;
  padding: 1.25rem;
  background: white;
}

.create-form,
.edit-form {
  display: grid;
  align-content: start;
  gap: 0.75rem;
}

input,
textarea,
button {
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  padding: 0.65rem 0.75rem;
  font: inherit;
}

textarea {
  resize: vertical;
}

button {
  border-color: #2563eb;
  color: white;
  background: #2563eb;
  cursor: pointer;
}

button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.secondary-button {
  border-color: #475569;
  background: #475569;
}

.error-message {
  margin-bottom: 1rem;
  color: #b91c1c;
}

.notes-list {
  display: grid;
  align-content: start;
  gap: 0.75rem;
}

.note-card {
  display: grid;
  gap: 0.5rem;
  width: 100%;
  border-top: 1px solid #e2e8f0;
  border-right: 0;
  border-bottom: 0;
  border-left: 0;
  border-radius: 0;
  padding-top: 1rem;
  color: inherit;
  text-align: left;
  background: transparent;
}

.note-card span {
  color: #475569;
  white-space: pre-wrap;
}

.edit-form {
  margin-top: 1.5rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
}

.danger-button {
  border-color: #b91c1c;
  background: #b91c1c;
}

@media (max-width: 760px) {
  .notes-layout {
    grid-template-columns: 1fr;
  }
}
</style>
