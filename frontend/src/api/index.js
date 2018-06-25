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

function GETUser (id, jsonOkCallback) {
  _GET('/api/users/' + id + '/', jsonOkCallback)
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

function POSTlab (name, description, scenarioId, preassessmentId, postassessmentId, allowedAttempts, jsonOkCallback) {
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      name: name,
      description: description,
      scenarioId: scenarioId,
      preassessmentId: preassessmentId,
      postassessmentId: postassessmentId,
      allowedAttempts: allowedAttempts
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

function POSTAssessment (atitle, adescription, questions, scores, jsonOkCallback) {
  console.log('API client - POST /api/assessments/ - inputs:', atitle, adescription, questions, scores)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'atitle': atitle,
      'adescription': adescription,
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

function GETAssessment (id, jsonOkCallback) {
  _GET('/api/assessments/' + id + '/', jsonOkCallback)
}

function POSTQuestion (qkind, qtitle, qtext, answers, correct, feedback, jsonOkCallback) {
  console.log('API client - POST /api/questions/ - inputs:', qkind, qtitle, qtext, answers, correct, feedback)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'qkind': qkind,
      'qtitle': qtitle,
      'qtext': qtext,
      'answers': answers,
      'correct': correct,
      'feedback': feedback
    })
  }
  console.log('API client - POST /api/questions/ - body:', options.body)

  fetch(API_SERVER + '/api/questions/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function LISTQuestions (jsonOkCallback) {
  _GET('/api/questions/', jsonOkCallback)
}

function GETQuestion (id, jsonOkCallback) {
  _GET('/api/questions/' + id + '/', jsonOkCallback)
}

function POSTReports (student, labname, assessmentid, answers, starttime, endtime, attemptNum, jsonOkCallback) {
  console.log('API client - POST /api/reports/ - inputs:', student, labname, assessmentid, answers, starttime, endtime)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'student': student,
      'labname': labname,
      'assessmentid': assessmentid,
      'answers': answers,
      'starttime': starttime,
      'endtime': endtime,
      'attemptNum': attemptNum
    })
  }
  console.log('API client - POST /api/reports/ - body:', options.body)

  fetch(API_SERVER + '/api/reports/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function LISTReports (jsonOkCallback) {
  _GET('/api/reports/', jsonOkCallback)
}

function GETReport (id, jsonOkCallback) {
  _GET('/api/reports/' + id + '/', jsonOkCallback)
}

function POSTGrade (student, reportid, points, feedback, needsgrading, jsonOkCallback) {
  console.log('API client - POST /api/grades/ - inputs:', student, reportid, points, feedback, needsgrading)
  let options = {
    headers: authHeaders(),
    method: 'POST',
    body: JSON.stringify({
      'student': student,
      'reportid': reportid,
      'points': points,
      'feedback': feedback,
      'needsgrading': needsgrading
    })
  }
  console.log('API client - POST /api/grades/ - body:', options.body)

  fetch(API_SERVER + '/api/grades/', options)
    .then(response => {
      if (response.ok) {
        response.json().then(jsonOkCallback)
      }
    })
}

function PATCHGrade (id, student, reportid, points, feedback, needsgrading, onSuccess, onFailed) {
  let options = {
    headers: authHeaders(),
    method: 'PATCH',
    body: JSON.stringify({
      student: student,
      reportid: reportid,
      points: points,
      feedback: feedback,
      needsgrading: needsgrading
    })
  }

  fetch(API_SERVER + '/api/grades/' + id + '/', options).then(response => {
    if (response.ok) {
      response.json().then(onSuccess)
    } else {
      response.json().then(onFailed)
    }
  })
}

function LISTGrades (jsonOkCallback) {
  _GET('/api/grades/', jsonOkCallback)
}

function GETGrade (id, jsonOkCallback) {
  _GET('/api/grades/' + id + '/', jsonOkCallback)
}

export {
  login,
  GETUserSelf,
  LISTusers,
  POSTUser,
  GETUser,
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
  LISTAssessments,
  GETAssessment,

  POSTQuestion,
  LISTQuestions,
  GETQuestion,

  POSTReports,
  LISTReports,
  GETReport,

  POSTGrade,
  GETGrade,
  LISTGrades,
  PATCHGrade
}
