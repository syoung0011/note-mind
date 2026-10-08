import { apiUrl } from '@/services/api'
import { getToken } from '@/services/auth'

export async function askQuestion(question) {
  const response = await fetch(apiUrl('/api/chat'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify({ question }),
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    const error = new Error(typeof data?.detail === 'string'
      ? data.detail
      : '问答请求失败，请稍后重试')
    error.status = response.status
    throw error
  }

  return response.json()
}
