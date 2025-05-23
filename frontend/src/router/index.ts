import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'layout',
    component: () => import('../layout/index.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'cases',
        name: 'cases',
        component: () => import('../views/cases/CaseList.vue')
      },
      {
        path: 'cases/create',
        name: 'case-create',
        component: () => import('../views/cases/CaseForm.vue')
      },
      {
        path: 'cases/:id',
        name: 'case-edit',
        component: () => import('../views/cases/CaseForm.vue')
      },
      {
        path: 'environments',
        name: 'environments',
        component: () => import('../views/environments/EnvironmentList.vue'),
        meta: { title: '环境管理' }
      },
      {
        path: 'environments/create',
        name: 'environment-create',
        component: () => import('../views/environments/EnvironmentForm.vue')
      },
      {
        path: 'environments/:id',
        name: 'environment-edit',
        component: () => import('../views/environments/EnvironmentForm.vue')
      },
      {
        path: 'executions',
        name: 'executions',
        component: () => import('../views/executions/ExecutionList.vue')
      },
      {
        path: '/executions/config',
        name: 'execution-config',
        component: () => import('../views/executions/ExecutionConfig.vue')
      },
      {
        path: '/executions/:id',
        name: 'execution-detail',
        component: () => import('../views/executions/ExecutionDetail.vue')
      },
      {
        path: 'reports',
        name: 'reports',
        component: () => import('../views/reports/ReportList.vue'),
        meta: { title: '测试报告' }
      },
      {
        path: 'reports/:id',
        name: 'report-detail',
        component: () => import('../views/reports/ReportDetail.vue'),
        meta: { title: '报告详情' }
      },
      {
        path: 'modules',
        name: 'modules',
        component: () => import('../views/modules/ModuleList.vue'),
        meta: { title: '模块管理' }
      },
      {
        path: 'modules/form',
        name: 'module-form',
        component: () => import('../views/modules/ModuleForm.vue'),
        meta: { title: '模块编辑' }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 