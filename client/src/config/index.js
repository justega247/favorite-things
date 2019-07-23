import dotenv from 'dotenv'

dotenv.config()

const { BASE_URL } = process.env

export default {
  apiUrl: process.env.NODE_ENV === 'production'
    ? BASE_URL : 'http://127.0.0.1:8000/api/v1'
}
