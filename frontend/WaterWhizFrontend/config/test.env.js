'use strict'
const merge = require('webpack-merge')
const devEnv = require('./prod.env')

module.exports = merge(devEnv, {
  NODE_ENV: '"testing"',
  ENV_NAME: '"Testing environment"',
  API_PREFIX: '"/api"' // API prefix
})
