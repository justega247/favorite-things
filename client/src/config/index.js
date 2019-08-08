export default {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'http://ec2-3-15-160-46.us-east-2.compute.amazonaws.com/api/v1' : 'http://127.0.0.1:8000/api/v1'
}
