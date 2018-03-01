import store from '@/store'

let API_SERVER = 'http://localhost:5000'
if (process.env.NODE_ENV === 'production') {
  API_SERVER = 'http://172.16.100.4:5002'
}

function authHeaders () {
  return {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': store.state.auth.token,
    'Email': store.state.auth.email
  }
}

// TODO: reuse this _GET in all other Get methods
function _GET (path, jsonOkCallback, jsonErrorCallback = null) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(`${API_SERVER}${path}`, options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      } else {
        if (jsonErrorCallback !== null) {
          response.json().then(jsonErrorCallback)
        }
      }
    })
}

function login (email, password) {
  let options = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify({
      'email': email,
      'password': password
    })
  }
  return fetch(API_SERVER + '/auth/tokens/', options)
}

function GETUserSelf (jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(API_SERVER + '/api/users/self', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function POSTUser (email, password, fullname, permissionGroups, jsonOkCallback) {
  console.log('API client - POST /api/users/ - inputs:', email, password, fullname, permissionGroups)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'fullname': fullname,
      'email': email,
      'password': password,
      'permissionGroups': permissionGroups
    })
  }
  console.log('API client - POST /api/users/ - body:', options.body)

  fetch(API_SERVER + '/api/users/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function SEARCHuser (searchTerm, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      searchTerm: searchTerm
    })
  }
  fetch(API_SERVER + '/api/users/search', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function LISTusers (jsonOkCallback) {
  _GET('/api/users/', jsonOkCallback)
}

function LISTscenarios (queries, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  let path = '/api/scenarios/'
  if (queries) {
    path = path + queries
  }
  fetch(API_SERVER + path, options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function GETscenario (id, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(API_SERVER + '/api/scenarios/' + id + '/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function POSTscenario (name, description, sgRules, isPublic, topo, onSuccess, onFailed) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      name: name,
      description: description,
      sgRules: sgRules,
      isPublic: isPublic,
      topo: topo
    })
  }

  fetch(API_SERVER + '/api/scenarios/', options).then(response => {
    if (response.ok) {
      response.json().then(onSuccess)
    } else {
      response.json().then(onFailed)
    }
  })
}

function PATCHscenario (name, description, sgRules, isPublic, topo, id, onSuccess, onFailed) {
  let options = {
    headers: authHeaders(),
    method: 'PATCH',
    body: JSON.stringify({
      name: name,
      description: description,
      sgRules: sgRules,
      isPublic: isPublic,
      topo: topo
    })
  }

  fetch(API_SERVER + '/api/scenarios/' + id + '/', options).then(response => {
    if (response.ok) {
      response.json().then(onSuccess)
    } else {
      response.json().then(onFailed)
    }
  })
}

function GETlab (labId, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(API_SERVER + '/api/labs/' + labId + '/', options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}

function POSTlab (name, description, scenarioId, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      name: name,
      description: description,
      scenarioId: scenarioId
    })
  }
  fetch(API_SERVER + '/api/labs/', options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}

function LISTlabs (jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(API_SERVER + '/api/labs/', options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}

function DEPLOYlab (id, cloudConfigId, users, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      cloudConfigId: cloudConfigId,
      users: users
    })
  }
  fetch(`${API_SERVER}/api/labs/${id}/deploy`, options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}

function DESTROYlab (id, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST'
  }
  fetch(`${API_SERVER}/api/labs/${id}/destroy`, options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}
function POSTcloudconfig (cloudDetail, provider, labId, jsonOkCallback, jsonErrorCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      cloudDetail: cloudDetail,
      provider: provider,
      labId: labId
    })
  }
  fetch(API_SERVER + '/api/cloudconfigs/', options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      } else {
        response.json()
          .then(jsonErrorCallback)
      }
    })
}

function GETslice (id, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'GET'
  }
  fetch(`${API_SERVER}/api/slices/${id}/`, options)
    .then(response => {
      if (response.ok) {
        response.json()
          .then(jsonOkCallback)
      }
    })
}

function LISTslices (jsonOkCallback) {
  _GET('/api/slices/', jsonOkCallback)
}

function LISTInstanceConfigurations (jsonOkCallback) {
  _GET('/api/configurations/?type=instance', jsonOkCallback)
}

function LISTRouterConfigurations (jsonOkCallback) {
  _GET('/api/configurations/?type=router', jsonOkCallback)
}

function LISTFlavors (jsonOkCallback) {
  _GET('/api/flavors/', jsonOkCallback)
}

// Functions for Assessment module

function POSTAssessment (title, description, questions, scores, jsonOkCallback) {
  console.log('API client - POST /api/assessments/ - inputs:', title, description, questions, scores)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'atitle': title,
      'adescription': description,
      'questions': questions,
      'scores': scores
    })
  }
  console.log('API client - POST /api/assessments/ - body:', options.body)

  fetch(API_SERVER + '/api/assessments/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function LISTAssessments (jsonOkCallback) {
  _GET('/api/assessments/', jsonOkCallback)
}

export {
  login,
  GETUserSelf,
  LISTusers,
  POSTUser,
  SEARCHuser,

  GETscenario,
  LISTscenarios,
  POSTscenario,
  PATCHscenario,

  GETlab,
  POSTlab,
  LISTlabs,
  DEPLOYlab,
  DESTROYlab,

  POSTcloudconfig,

  GETslice,
  LISTslices,

  LISTInstanceConfigurations,
  LISTRouterConfigurations,

  LISTFlavors,

  POSTAssessment,
  LISTAssessments

}
