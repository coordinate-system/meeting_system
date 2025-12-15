// src/utils/time.js

/**
 * 将后端返回的 UTC 时间字符串
 * 转换为本地时间并格式化
 *
 * @param {string | null} timeStr
 * @param {string} format 默认 YYYY-MM-DD HH:mm:ss
 */
export function formatTime(timeStr, format = 'YYYY-MM-DD HH:mm:ss') {
    if (!timeStr) return ''
  
    const date = new Date(timeStr)
  
    const pad = n => String(n).padStart(2, '0')
  
    const map = {
      YYYY: date.getFullYear(),
      MM: pad(date.getMonth() + 1),
      DD: pad(date.getDate()),
      HH: pad(date.getHours()),
      mm: pad(date.getMinutes()),
      ss: pad(date.getSeconds())
    }
  
    return format.replace(
      /YYYY|MM|DD|HH|mm|ss/g,
      match => map[match]
    )
  }
  