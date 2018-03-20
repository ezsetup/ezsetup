import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/authentication/Login'

import LabsManagement from '@/components/labs/LabsManagement'
import NewLab from '@/components/labs/NewLab'
import Lab from '@/components/labs/Lab'

import Slice from '@/components/slices/Slice'

import ScenariosManagement from '@/components/scenarios/ScenariosManagement'
import ScenarioEditor from '@/components/scenarios/ScenarioEditor'

import UsersManagement from '@/components/users/UsersManagement'
import UserCreation from '@/components/users/UserCreation'

import WorkSpace from '@/components/workspace/WorkSpace'

import store from '@/store'
// import Cookies from 'js-cookie'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'index',
      redirect: to => store.getters.isRoot ? '/labs' : '/workspace',
      meta: {
        authRequired: true
      }
    },
    {
      path: '/workspace',
      component: WorkSpace,
      name: 'WorkSpace',
      meta: {
        rootRequired: false,
        authRequired: true
      }
    },
    {
      path: '/labs',
      component: LabsManagement,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/users',
      component: UsersManagement,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/users/new',
      name: 'NewUser',
      component: UserCreation,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/scenarios',
      component: ScenariosManagement,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/scenarios/new',
      name: 'NewScenario',
      component: ScenarioEditor,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/scenarios/:id',
      name: 'ScenarioEditor',
      component: ScenarioEditor,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/labs/new',
      name: 'NewLab',
      component: NewLab,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/labs/:id',
      name: 'Lab',
      component: Lab,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/slices/:sliceId',
      name: 'Slice',
      component: Slice,
      meta: {
        authRequired: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.authRequired && !store.state.auth) {
    return next({ path: '/login' })
  }
  if (to.meta.rootRequired && !store.getters.isRoot) {
    return next({ path: '/' })
  }
  next()
})

export default router
