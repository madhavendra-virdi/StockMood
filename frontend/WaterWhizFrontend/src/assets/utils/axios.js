import axios from 'axios'
axios.defaults.headers.common['Content-Type'] = 'application/json;charset=UTF-8'
export default axios.create({
  timeout: 30000
})
