import axios from 'axios'
import { trim } from './util'
axios.defaults.headers.common['Content-Type'] = 'application/json;charset=UTF-8'
const axiosInstance = axios.create({
  baseURL: '/api',
  // Request timeout
  timeout: 900000
})

// Add a request interceptor
axiosInstance.interceptors.request.use(function (config) {
  // Parameter whitespace
  if (config.trim === true) {
    if (config.data != null) {
      config.data = trim(config.data)
    }
    if (config.params != null) {
      config.params = trim(config.params)
    }
  }
  return config
}, function (error) {
  // What to do about request errors
  return Promise.reject(error)
})

// Add a response interceptor
axiosInstance.interceptors.response.use(response => {
  // Request failed
  if (response.status !== 200) {
    return Promise.reject(response.data)
  }
  // Not logged in
  if (response.data.code === 401) {
    window.location.href = '/#/login'
  }
  // Service failure
  if (response.data.code !== 200) {
    return Promise.reject(response.data)
  }
  return response.data.data
}, function (error) {
  // What to do about response errors
  return Promise.reject(error)
})

export default axiosInstance
