<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { logout } from "@/services/auth";
import { askQuestion } from "@/services/chat";
import {
  createNote,
  deleteNote,
  getNote,
  listNotes,
  updateNote,
} from "@/services/notes";

const router = useRouter();
const notes = ref([]);
const selectedNote = ref(null);
const editTitle = ref("");
const editContent = ref("");
const isLoading = ref(false);
const isCreating = ref(false);
const isSaving = ref(false);
const isDeleting = ref(false);
const isSelecting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const listError = ref("");
const question = ref("");
const chatResult = ref(null);
const chatError = ref("");
const isAsking = ref(false);
const isBusy = computed(
  () =>
    isLoading.value ||
    isCreating.value ||
    isSaving.value ||
    isDeleting.value ||
    isSelecting.value,
);

function clearNoteFeedback() {
  errorMessage.value = "";
  successMessage.value = "";
}

function startNewNote() {
  if (isBusy.value) return;
  selectedNote.value = null;
  editTitle.value = "";
  editContent.value = "";
  clearNoteFeedback();
}

function handleSave() {
  if (isBusy.value) return;
  return selectedNote.value ? handleUpdate() : handleCreate();
}

function isNoteSelected(noteId) {
  return selectedNote.value?.id === noteId;
}

async function handleAsk() {
  const submittedQuestion = question.value.trim();
  if (isAsking.value || !submittedQuestion) return;
  chatError.value = "";
  chatResult.value = null;
  isAsking.value = true;

  try {
    chatResult.value = await askQuestion(submittedQuestion);
  } catch (error) {
    if (error.status === 401) {
      await handleRequestError(error);
    } else {
      chatError.value =
        error instanceof TypeError
          ? "无法连接问答服务，请检查网络后重试"
          : error.message || "问答失败，请稍后重试";
    }
  } finally {
    isAsking.value = false;
  }
}

async function loadNotes() {
  if (isBusy.value) return;
  clearNoteFeedback();
  listError.value = "";
  isLoading.value = true;

  try {
    notes.value = await listNotes();
  } catch (error) {
    if (error.status === 401) {
      await handleRequestError(error);
    } else {
      listError.value =
        error instanceof TypeError
          ? "无法连接笔记服务，请检查网络后重试"
          : error.message || "加载笔记失败，请重试";
    }
  } finally {
    isLoading.value = false;
  }
}

async function handleCreate() {
  clearNoteFeedback();
  isCreating.value = true;

  try {
    const createdNote = await createNote({
      title: editTitle.value,
      content: editContent.value,
    });
    notes.value.unshift(createdNote);
    selectedNote.value = createdNote;
    editTitle.value = createdNote.title;
    editContent.value = createdNote.content;
    successMessage.value = "笔记已创建";
  } catch (error) {
    await handleRequestError(error);
  } finally {
    isCreating.value = false;
  }
}

async function selectNote(noteId) {
  if (isBusy.value) return;
  clearNoteFeedback();
  isSelecting.value = true;

  try {
    const note = await getNote(noteId);
    selectedNote.value = note;
    editTitle.value = note.title;
    editContent.value = note.content;
  } catch (error) {
    await handleRequestError(error);
  } finally {
    isSelecting.value = false;
  }
}

async function handleUpdate() {
  clearNoteFeedback();
  isSaving.value = true;

  try {
    const updatedNote = await updateNote(selectedNote.value.id, {
      title: editTitle.value,
      content: editContent.value,
    });
    const noteIndex = notes.value.findIndex(
      (note) => note.id === updatedNote.id,
    );

    selectedNote.value = updatedNote;
    if (noteIndex !== -1) {
      notes.value[noteIndex] = updatedNote;
    }
    successMessage.value = "修改已保存！";
  } catch (error) {
    await handleRequestError(error);
  } finally {
    isSaving.value = false;
  }
}

async function handleDelete() {
  if (isBusy.value || !selectedNote.value) return;
  if (!window.confirm("确定要删除这篇笔记吗？此操作无法撤销。")) {
    return;
  }

  const noteId = selectedNote.value.id;
  clearNoteFeedback();
  isDeleting.value = true;

  try {
    await deleteNote(noteId);
    notes.value = notes.value.filter((note) => note.id !== noteId);
    selectedNote.value = null;
    editTitle.value = "";
    editContent.value = "";
    successMessage.value = "笔记已删除";
  } catch (error) {
    await handleRequestError(error);
  } finally {
    isDeleting.value = false;
  }
}

async function handleRequestError(error) {
  if (error.status === 401) {
    logout();
    await router.replace({ name: "login", query: { reason: "expired" } });
    return;
  }

  errorMessage.value =
    error instanceof TypeError
      ? "无法连接笔记服务，请检查网络或稍后重试"
      : error.message || "请求失败，请稍后重试";
}

async function handleLogout() {
  logout();
  await router.replace({ name: "login" });
}

onMounted(loadNotes);
</script>

<template>
  <main class="notes-page">
    <header class="page-header">
      <div>
        <h1>我的笔记</h1>
      </div>
      <button class="secondary-button" type="button" @click="handleLogout">
        退出登录
      </button>
    </header>

    <p v-if="errorMessage" class="error-message" role="alert">
      {{ errorMessage }}
    </p>
    <p v-if="successMessage" class="success-message" role="status">
      {{ successMessage }}
    </p>

    <section class="notes-layout">
      <section class="panel notes-list" aria-live="polite">
        <h2>笔记列表（{{ notes.length }}）</h2>
        <button type="button" :disabled="isBusy" @click="startNewNote">
          新建笔记
        </button>
        <p v-if="isLoading" role="status">正在加载笔记…</p>
        <div v-else-if="listError">
          <p class="error-message" role="alert">{{ listError }}</p>
          <button type="button" :disabled="isBusy" @click="loadNotes">
            重新加载
          </button>
        </div>
        <p v-else-if="notes.length === 0" class="muted-text">
          还没有笔记。在编辑区写下第一篇笔记，保存后就会出现在这里。
        </p>
        <button
          v-for="note in notes"
          v-else
          :key="note.id"
          class="note-card"
          :class="{ 'note-card--selected': isNoteSelected(note.id) }"
          :aria-pressed="isNoteSelected(note.id)"
          type="button"
          :disabled="isBusy"
          @click="selectNote(note.id)"
        >
          <strong>{{ note.title }}</strong>
          <span>{{ note.content }}</span>
        </button>
      </section>
      <form class="panel edit-form" @submit.prevent="handleSave">
        <h2>{{ selectedNote ? "编辑笔记" : "创建笔记" }}</h2>
        <p v-if="!selectedNote && !isSelecting" class="muted-text">
          填写标题和正文后创建笔记，或从列表选择已有笔记继续编辑。切换笔记会放弃未保存的输入。
        </p>
        <p v-if="isSelecting" role="status">正在读取笔记…</p>

        <label for="edit-title">标题</label>
        <input
          id="edit-title"
          v-model="editTitle"
          maxlength="200"
          :disabled="isBusy"
          required
        />

        <label for="edit-content">正文</label>
        <textarea
          id="edit-content"
          v-model="editContent"
          rows="10"
          :disabled="isBusy"
          required
        ></textarea>

        <div class="form-actions">
          <button type="submit" :disabled="isBusy">
            {{
              isCreating || isSaving
                ? "正在保存…"
                : selectedNote
                  ? "保存修改"
                  : "创建笔记"
            }}
          </button>
          <button
            class="danger-button"
            v-if="selectedNote"
            type="button"
            :disabled="isBusy"
            @click="handleDelete"
          >
            {{ isDeleting ? "正在删除…" : "删除笔记" }}
          </button>
        </div>
      </form>
      <section class="panel chat-panel" aria-labelledby="chat-heading">
        <h2 id="chat-heading">AI 笔记问答</h2>
        <p class="muted-text">
          检索你已保存的全部笔记，不限于当前选中笔记。未保存的草稿不会参与回答。
        </p>
        <form class="chat-form" @submit.prevent="handleAsk">
          <label for="chat-question">你的问题</label>
          <textarea
            id="chat-question"
            v-model="question"
            rows="4"
            maxlength="2000"
            :disabled="isAsking"
            required
          ></textarea>
          <button type="submit" :disabled="isAsking || !question.trim()">
            {{ isAsking ? "正在回答…" : "向笔记提问" }}
          </button>
        </form>
        <p v-if="isAsking" role="status">正在检索笔记并生成回答，请稍候。</p>
        <p v-if="chatError" class="error-message" role="alert">
          {{ chatError }}
        </p>
        <div v-if="chatResult" class="chat-result" aria-live="polite">
          <h3>回答</h3>
          <p class="answer-text">{{ chatResult.answer }}</p>
          <h3>引用来源</h3>
          <p v-if="chatResult.citations.length === 0" class="muted-text">
            本次回答没有引用来源。
          </p>
          <details
            v-for="citation in chatResult.citations"
            :key="`${citation.note_id}-${citation.chunk_index}`"
            class="citation"
          >
            <summary>
              {{ citation.note_title }} · 片段 {{ citation.chunk_index + 1 }}
            </summary>
            <p class="answer-text">{{ citation.content }}</p>
          </details>
        </div>
        <p v-else-if="!isAsking && !chatError" class="muted-text">
          先保存学习笔记，再提出一个相关问题。
        </p>
      </section>
    </section>
  </main>
</template>

<style scoped>
.notes-page {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 2rem var(--space-page);
}

.page-header {
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-header h1,
.panel h2 {
  margin: 0 0 0.75rem;
}

.notes-layout {
  display: grid;
  grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.2fr) minmax(0, 1fr);
  align-items: start;
  gap: 1.5rem;
}

.panel {
  border: 1px solid #dbe3ef;
  min-width: 0;
  border-radius: var(--radius-panel);
  padding: 1.25rem;
  background: var(--color-surface);
}

.edit-form {
  display: grid;
  align-content: start;
  gap: 0.75rem;
}

.chat-panel,
.chat-form,
.chat-result {
  display: grid;
  gap: 0.75rem;
}

.answer-text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.citation {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
}

.citation summary {
  cursor: pointer;
  overflow-wrap: anywhere;
}

.error-message {
  margin-bottom: 1rem;
}

.success-message {
  margin-bottom: 1rem;
  color: #166534;
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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
  padding: 0.75rem;
  color: inherit;
  text-align: left;
  background: transparent;
}

.note-card span {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  color: var(--color-muted);
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}

.note-card strong {
  overflow-wrap: anywhere;
}

.muted-text {
  margin: 0;
  color: var(--color-muted);
  overflow-wrap: anywhere;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.note-card:hover:not(:disabled) {
  background: var(--color-background);
}

.note-card.note-card--selected {
  border-color: var(--color-primary);
  background: var(--color-background);
  box-shadow: inset 3px 0 0 var(--color-primary);
}

@media (max-width: 1000px) {
  .notes-layout {
    grid-template-columns: 1fr;
  }
}
</style>
