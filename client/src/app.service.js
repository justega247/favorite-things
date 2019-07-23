import axios from 'axios'
import { backendRoutes } from './constants/routes'
import config from './config'

axios.defaults.baseURL = config.apiUrl

const appService = {
  addCategory (categoryData) {
    return new Promise((resolve, reject) => {
      axios.post(`${config.apiUrl}${backendRoutes.CATEGORY}`, categoryData)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  },
  getCategories () {
    return new Promise((resolve, reject) => {
      axios.get(`${config.apiUrl}${backendRoutes.CATEGORY}`)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  }
}

export default appService
