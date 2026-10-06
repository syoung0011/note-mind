import { getToken } from '@/services/auth'
import { apiUrl } from '@/services/api'

async function requestNotes(path = '', options = {}) {
  const token = getToken()
  const response = await fetch(apiUrl(`/api/notes${path}`), {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    const error = new Error(errorData?.detail ?? '笔记请求失败，请稍后重试')
    error.status = response.status
    throw error
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export function listNotes() {
  return requestNotes()
}

export function getNote(noteId) {
  return requestNotes(`/${noteId}`)
}

export function createNote(note) {
  return requestNotes('', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(note),
  })
}

export function updateNote(noteId, note) {
  return requestNotes(`/${noteId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(note),
  })
}

export function deleteNote(noteId) {
  return requestNotes(`/${noteId}`, {
    method: 'DELETE',
  })
}
