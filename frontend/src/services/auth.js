import { ref } from 'vue'

import { apiUrl } from '@/services/api'

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
    const response = await fetch(apiUrl('/api/auth/me'), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 401) {
      clearToken()
      currentUser.value = null
      return null
    }

    if (!response.ok) {
      throw new Error('暂时无法确认登录状态，请稍后重试')
    }

    currentUser.value = await response.json()
    return currentUser.value
  } catch (error) {
    currentUser.value = null
    throw error
  } finally {
    isAuthReady.value = true
  }
}

export function logout() {
  clearToken()
  currentUser.value = null
}

export async function register(username, password) {
  const requestBody = JSON.stringify({ username, password })

  const response = await fetch(apiUrl('/api/auth/register'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: requestBody,
  })

  if (!response.ok) {
    if (response.status === 409) {
      throw new Error('用户名已被使用，请换一个')
    }
    if (response.status === 422) {
      throw new Error('请检查用户名和密码是否符合要求')
    }
    throw new Error('注册失败，请稍后重试')
  }

  return response.json()
}

export async function login(username, password) {
  const formData = new URLSearchParams()

  formData.set('username', username)
  formData.set('password', password)

  const response = await fetch(apiUrl('/api/auth/login'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  })

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('用户名或密码错误')
    }
    const errorData = await response.json().catch(() => null)
    throw new Error(typeof errorData?.detail === 'string'
      ? errorData.detail
      : '登录失败，请稍后重试')
  }

  const tokenData = await response.json()
  localStorage.setItem(TOKEN_KEY, tokenData.access_token)

  const user = await restoreAuth()

  if (!user) throw new Error('登录状态验证失败，请重新登录')
  return tokenData.access_token
}
