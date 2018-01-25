import store from '@/store'

let headers = () => {
  if (store.state.auth !== null) {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': store.state.auth.token,
      'Email': store.state.auth.email
    }
  } else {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }
}

let optionsGET = () => {
  return {
    method: 'GET',
    headers: headers()
  }
}

let optionsPOST = () => {
  return {
    method: 'POST',
    headers: headers()
  }
}

export {
  optionsGET,
  optionsPOST
}
