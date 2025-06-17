// Verify mobile phone number
export function checkMobile (rule, value, callback) {
  if (value == null || value.trim() === '') {
    callback()
    return
  }
  if (!/^1\d{10}$/.test(value)) {
    callback(new Error('The mobile phone number format is incorrect'))
    return
  }
  callback()
}

// Verification mailbox
export function checkEmail (rule, value, callback) {
  if (value == null || value.trim() === '') {
    callback()
    return
  }
  if (!/^\S+@\S+\.\S+$/.test(value)) {
    callback(new Error('The mailbox format is incorrect'))
    return
  }
  callback()
}
