// TODO: remove this file
let API_SERVER = 'http://localhost:5000'
if (process.env.NODE_ENV === 'production') {
  API_SERVER = 'http://172.16.100.4:5002'
}
export {
  API_SERVER
}
