import request from '../utils/request'

// Interface Definition Example
export function demo (data) {
  return request.post('/demo', data)
}
