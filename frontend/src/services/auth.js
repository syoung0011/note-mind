import { ref } from 'vue'

const TOKEN_KEY = 'notemind_access_token'

export const currentUser = ref(null)
export const isAuthReady = ref(false)

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export async function restoreAuth() {
  const token = getToken()

  if (!token) {
    currentUser.value = null
    isAuthReady.value = true
    return null
  }

  try {
    const response = await fetch('/api/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('登录状态已失效')
    }

    currentUser.value = await response.json()
    return currentUser.value
  } catch (error) {
    clearToken()
    currentUser.value = null
    return null
  } finally {
    isAuthReady.value = true
  }
}

export function logout() {
  clearToken()
  currentUser.value = null
}

export async function login(username, password) {
  const formData = new URLSearchParams()

  formData.set('username', username)
  formData.set('password', password)

  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new Error(errorData?.detail ?? '登录失败，请稍后重试')
  }

  const tokenData = await response.json()
  localStorage.setItem(TOKEN_KEY, tokenData.access_token)

  await restoreAuth()

  return tokenData.access_token
}
