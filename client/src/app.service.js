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
  },
  getCategoryFavorites ({ categoryId, limit, offset }) {
    return new Promise((resolve, reject) => {
      axios.get(`${config.apiUrl}${backendRoutes.CATEGORY_FAVORITES}/${categoryId}?limit=${limit}&offset=${offset}`)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  },
  getCategory (categoryId) {
    return new Promise((resolve, reject) => {
      axios.get(`${config.apiUrl}${backendRoutes.CATEGORY}${categoryId}/`)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  },
  deleteFavorite (favoriteId) {
    return new Promise((resolve, reject) => {
      axios.delete(`${config.apiUrl}${backendRoutes.FAVORITE}${favoriteId}`)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  },
  addFavorite (favoriteData) {
    return new Promise((resolve, reject) => {
      axios.post(`${config.apiUrl}${backendRoutes.FAVORITE}`, favoriteData)
        .then(response => {
          resolve(response.data)
        }).catch(err => {
          reject(err)
        })
    })
  }
}

export default appService
