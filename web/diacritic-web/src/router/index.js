import Vue from 'vue'
import Router from 'vue-router'
import Spell from '@/components/Spell'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Spell',
      component: Spell
    }
  ]
})
