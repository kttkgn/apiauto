<template>
  <div class="execution-detail">
    <!-- 基本信息 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="用例名称">{{ executionInfo.name }}</el-descriptions-item>
        <el-descriptions-item label="执行范围">
          <el-tag :type="getScopeType(executionInfo.scope)">{{ getScopeLabel(executionInfo.scope) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="环境">{{ executionInfo.environment }}</el-descriptions-item>
        <el-descriptions-item label="执行人">{{ executionInfo.executor }}</el-descriptions-item>
        <el-descriptions-item label="执行时间">{{ executionInfo.created_at }}</el-descriptions-item>
        <el-descriptions-item label="执行状态">
          <el-tag :type="getStatusType(executionInfo.status)">{{ getStatusLabel(executionInfo.status) }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 执行进度（执行中时显示） -->
    <template v-if="executionInfo.status === 'running'">
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>执行进度</span>
          </div>
        </template>
        <div class="progress-info">
          <el-progress 
            :percentage="executionProgress.percentage" 
            :status="executionProgress.status"
          />
          <div class="progress-stats">
            <div class="stat-item">
              <span class="label">总用例数：</span>
              <span class="value">{{ executionProgress.total }}</span>
            </div>
            <div class="stat-item">
              <span class="label">已完成：</span>
              <span class="value">{{ executionProgress.completed }}</span>
            </div>
            <div class="stat-item">
              <span class="label">通过：</span>
              <span class="value success">{{ executionProgress.passed }}</span>
            </div>
            <div class="stat-item">
              <span class="label">失败：</span>
              <span class="value danger">{{ executionProgress.failed }}</span>
            </div>
            <div class="stat-item">
              <span class="label">执行时间：</span>
              <span class="value">{{ executionProgress.duration }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 实时日志 -->
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>实时日志</span>
            <el-button type="primary" link @click="clearLogs">
              清空日志
            </el-button>
          </div>
        </template>
        <div class="log-container" ref="logContainer">
          <div v-for="(log, index) in executionLogs" :key="index" class="log-item">
            <span class="log-time">{{ log.time }}</span>
            <span :class="['log-level', log.level]">{{ log.level }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </el-card>
    </template>

    <!-- 执行结果列表（模块用例和全部用例时显示） -->
    <template v-if="executionInfo.scope !== 'single'">
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>执行结果列表</span>
          </div>
        </template>
        <el-table :data="executionResults" style="width: 100%">
          <el-table-column type="expand">
            <template #default="{ row }">
              <!-- 请求详情 -->
              <div class="case-detail">
                <h4>请求详情</h4>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="请求URL">{{ row.request.url }}</el-descriptions-item>
                  <el-descriptions-item label="请求方法">
                    <el-tag>{{ row.request.method }}</el-tag>
                  </el-descriptions-item>
                  <el-descriptions-item label="请求头">
                    <pre class="json-content">{{ formatJson(row.request.headers) }}</pre>
                  </el-descriptions-item>
                  <el-descriptions-item label="请求参数">
                    <pre class="json-content">{{ formatJson(row.request.params) }}</pre>
                  </el-descriptions-item>
                  <el-descriptions-item label="请求体">
                    <pre class="json-content">{{ formatJson(row.request.body) }}</pre>
                  </el-descriptions-item>
                </el-descriptions>

                <!-- 响应详情 -->
                <h4>响应详情</h4>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="响应状态码">
                    <el-tag :type="getStatusCodeType(row.response.status_code)">
                      {{ row.response.status_code }}
                    </el-tag>
                  </el-descriptions-item>
                  <el-descriptions-item label="响应头">
                    <pre class="json-content">{{ formatJson(row.response.headers) }}</pre>
                  </el-descriptions-item>
                  <el-descriptions-item label="响应体">
                    <pre class="json-content">{{ formatJson(row.response.body) }}</pre>
                  </el-descriptions-item>
                </el-descriptions>

                <!-- 断言结果 -->
                <h4>断言结果</h4>
                <el-table :data="row.assertions" style="width: 100%">
                  <el-table-column prop="name" label="断言项" min-width="200" />
                  <el-table-column prop="expected" label="预期值" min-width="200">
                    <template #default="{ row: assertion }">
                      <pre class="json-content">{{ formatJson(assertion.expected) }}</pre>
                    </template>
                  </el-table-column>
                  <el-table-column prop="actual" label="实际值" min-width="200">
                    <template #default="{ row: assertion }">
                      <pre class="json-content">{{ formatJson(assertion.actual) }}</pre>
                    </template>
                  </el-table-column>
                  <el-table-column prop="result" label="结果" width="100">
                    <template #default="{ row: assertion }">
                      <el-tag :type="assertion.result ? 'success' : 'danger'">
                        {{ assertion.result ? '通过' : '失败' }}
                      </el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="用例名称" min-width="200" />
          <el-table-column prop="api_name" label="接口名称" min-width="200" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>

    <!-- 单个用例的请求详情 -->
    <template v-else>
      <!-- 请求详情 -->
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>请求详情</span>
          </div>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="请求URL">{{ requestInfo.url }}</el-descriptions-item>
          <el-descriptions-item label="请求方法">
            <el-tag>{{ requestInfo.method }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="请求头">
            <pre class="json-content">{{ formatJson(requestInfo.headers) }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="请求参数">
            <pre class="json-content">{{ formatJson(requestInfo.params) }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="请求体">
            <pre class="json-content">{{ formatJson(requestInfo.body) }}</pre>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 响应详情 -->
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>响应详情</span>
          </div>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="响应状态码">
            <el-tag :type="getStatusCodeType(responseInfo.status_code)">
              {{ responseInfo.status_code }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="响应头">
            <pre class="json-content">{{ formatJson(responseInfo.headers) }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="响应体">
            <pre class="json-content">{{ formatJson(responseInfo.body) }}</pre>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 断言结果 -->
      <el-card class="detail-card">
        <template #header>
          <div class="card-header">
            <span>断言结果</span>
          </div>
        </template>
        <el-table :data="assertionResults" style="width: 100%">
          <el-table-column prop="name" label="断言项" min-width="200" />
          <el-table-column prop="expected" label="预期值" min-width="200">
            <template #default="{ row }">
              <pre class="json-content">{{ formatJson(row.expected) }}</pre>
            </template>
          </el-table-column>
          <el-table-column prop="actual" label="实际值" min-width="200">
            <template #default="{ row }">
              <pre class="json-content">{{ formatJson(row.actual) }}</pre>
            </template>
          </el-table-column>
          <el-table-column prop="result" label="结果" width="100">
            <template #default="{ row }">
              <el-tag :type="row.result ? 'success' : 'danger'">
                {{ row.result ? '通过' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

// 执行信息
const executionInfo = reactive({
  name: '',
  scope: '',
  environment: '',
  executor: '',
  created_at: '',
  status: ''
})

// 执行结果列表（模块用例和全部用例时使用）
const executionResults = ref([
  {
    id: 1,
    name: '用户登录接口测试',
    api_name: 'POST /api/login',
    status: 'success',
    request: {
      url: 'http://api.example.com/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xxx'
      },
      params: {
        version: 'v1'
      },
      body: {
        username: 'test',
        password: '123456'
      }
    },
    response: {
      status_code: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        code: 0,
        message: 'success',
        data: {
          token: 'xxx',
          user_id: 123
        }
      }
    },
    assertions: [
      {
        name: '状态码断言',
        expected: 200,
        actual: 200,
        result: true
      },
      {
        name: '响应体断言',
        expected: { code: 0, message: 'success' },
        actual: { code: 0, message: 'success' },
        result: true
      }
    ]
  },
  {
    id: 2,
    name: '订单创建接口测试',
    api_name: 'POST /api/orders',
    status: 'failed',
    request: {
      url: 'http://api.example.com/orders',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        product_id: 123,
        quantity: 1
      }
    },
    response: {
      status_code: 400,
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        code: 400,
        message: '参数错误'
      }
    },
    assertions: [
      {
        name: '状态码断言',
        expected: 200,
        actual: 400,
        result: false
      }
    ]
  }
])

// 请求信息
const requestInfo = reactive({
  url: '',
  method: '',
  headers: {},
  params: {},
  body: {}
})

// 响应信息
const responseInfo = reactive({
  status_code: 0,
  headers: {},
  body: {}
})

// 断言结果
const assertionResults = ref([
  {
    name: '状态码断言',
    expected: 200,
    actual: 200,
    result: true
  },
  {
    name: '响应体断言',
    expected: { code: 0, message: 'success' },
    actual: { code: 0, message: 'success' },
    result: true
  }
])

// 执行进度
const executionProgress = reactive({
  percentage: 0,
  status: 'active',
  total: 0,
  completed: 0,
  passed: 0,
  failed: 0,
  duration: '00:00:00'
})

// 执行日志
const executionLogs = ref<Array<{
  time: string,
  level: string,
  message: string
}>>([])

const logContainer = ref<HTMLElement | null>(null)

// 清空日志
const clearLogs = () => {
  executionLogs.value = []
}

// 添加日志
const addLog = (level: string, message: string) => {
  const now = new Date()
  const time = now.toLocaleTimeString()
  executionLogs.value.push({ time, level, message })
  // 自动滚动到底部
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

// 模拟执行进度更新
const simulateProgress = () => {
  if (executionInfo.status === 'running') {
    const interval = setInterval(() => {
      if (executionProgress.percentage < 100) {
        executionProgress.percentage += 10
        executionProgress.completed += 1
        if (Math.random() > 0.3) {
          executionProgress.passed += 1
          addLog('info', `用例 ${executionProgress.completed} 执行通过`)
        } else {
          executionProgress.failed += 1
          addLog('error', `用例 ${executionProgress.completed} 执行失败`)
        }
        // 更新执行时间
        const duration = new Date().getTime() - startTime
        executionProgress.duration = formatDuration(duration)
      } else {
        clearInterval(interval)
        executionInfo.status = 'success'
        addLog('info', '所有用例执行完成')
      }
    }, 1000)
  }
}

// 格式化执行时间
const formatDuration = (ms: number) => {
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  return `${hours.toString().padStart(2, '0')}:${(minutes % 60).toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`
}

// 记录开始时间
let startTime = 0

// 获取执行范围标签
const getScopeLabel = (scope: string) => {
  const map: Record<string, string> = {
    single: '单个用例',
    module: '模块用例',
    all: '全部用例'
  }
  return map[scope] || scope
}

// 获取执行范围类型
const getScopeType = (scope: string) => {
  const map: Record<string, string> = {
    single: '',
    module: 'success',
    all: 'warning'
  }
  return map[scope] || ''
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    success: '成功',
    failed: '失败',
    running: '执行中'
  }
  return map[status] || status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    success: 'success',
    failed: 'danger',
    running: 'warning'
  }
  return map[status] || ''
}

// 获取状态码类型
const getStatusCodeType = (code: number) => {
  if (code >= 200 && code < 300) return 'success'
  if (code >= 400 && code < 500) return 'warning'
  if (code >= 500) return 'danger'
  return ''
}

// 格式化JSON
const formatJson = (data: any) => {
  try {
    return JSON.stringify(data, null, 2)
  } catch {
    return data
  }
}

// 查看用例详情
const handleViewCaseDetail = (row: any) => {
  // TODO: 实现查看用例详情
  console.log('查看用例详情:', row)
}

// 获取执行详情
const fetchExecutionDetail = (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  const scope = route.query.scope || 'single'
  
  Object.assign(executionInfo, {
    name: '用户登录接口测试',
    scope: scope,
    environment: '开发环境',
    executor: '张三',
    created_at: '2024-03-20 10:00:00',
    status: 'running' // 设置为执行中状态
  })

  // 初始化执行进度
  Object.assign(executionProgress, {
    percentage: 0,
    status: 'active',
    total: scope === 'single' ? 1 : 10,
    completed: 0,
    passed: 0,
    failed: 0,
    duration: '00:00:00'
  })

  // 清空日志
  executionLogs.value = []
  
  // 记录开始时间
  startTime = new Date().getTime()
  
  // 添加开始日志
  addLog('info', '开始执行用例')
  
  // 开始模拟进度更新
  simulateProgress()

  if (scope === 'single') {
    // 单个用例的数据
    Object.assign(requestInfo, {
      url: 'http://api.example.com/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xxx'
      },
      params: {
        version: 'v1'
      },
      body: {
        username: 'test',
        password: '123456'
      }
    })

    Object.assign(responseInfo, {
      status_code: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        code: 0,
        message: 'success',
        data: {
          token: 'xxx',
          user_id: 123
        }
      }
    })

    assertionResults.value = [
      {
        name: '状态码断言',
        expected: 200,
        actual: 200,
        result: true
      },
      {
        name: '响应体断言',
        expected: { code: 0, message: 'success' },
        actual: { code: 0, message: 'success' },
        result: true
      }
    ]
  } else {
    // 模块用例或全部用例的数据
    executionResults.value = [
      {
        id: 1,
        name: '用户登录接口测试',
        api_name: 'POST /api/login',
        status: 'success',
        request: {
          url: 'http://api.example.com/login',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer xxx'
          },
          params: {
            version: 'v1'
          },
          body: {
            username: 'test',
            password: '123456'
          }
        },
        response: {
          status_code: 200,
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            code: 0,
            message: 'success',
            data: {
              token: 'xxx',
              user_id: 123
            }
          }
        },
        assertions: [
          {
            name: '状态码断言',
            expected: 200,
            actual: 200,
            result: true
          },
          {
            name: '响应体断言',
            expected: { code: 0, message: 'success' },
            actual: { code: 0, message: 'success' },
            result: true
          }
        ]
      },
      {
        id: 2,
        name: '订单创建接口测试',
        api_name: 'POST /api/orders',
        status: 'failed',
        request: {
          url: 'http://api.example.com/orders',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            product_id: 123,
            quantity: 1
          }
        },
        response: {
          status_code: 400,
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            code: 400,
            message: '参数错误'
          }
        },
        assertions: [
          {
            name: '状态码断言',
            expected: 200,
            actual: 400,
            result: false
          }
        ]
      }
    ]
  }
}

// 初始化
onMounted(() => {
  const id = route.params.id
  if (id) {
    fetchExecutionDetail(id as string)
  }
})
</script>

<style scoped>
.execution-detail {
  height: 100%;
  padding: 20px;
  overflow-y: auto;
}

.detail-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.json-content {
  margin: 0;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

.case-detail {
  padding: 20px;
}

.case-detail h4 {
  margin: 20px 0 10px;
  font-size: 16px;
  color: #606266;
}

.case-detail h4:first-child {
  margin-top: 0;
}

.progress-info {
  padding: 20px;
}

.progress-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-item .label {
  color: #606266;
}

.stat-item .value {
  font-weight: bold;
}

.stat-item .value.success {
  color: #67c23a;
}

.stat-item .value.danger {
  color: #f56c6c;
}

.log-container {
  height: 300px;
  overflow-y: auto;
  background-color: #1e1e1e;
  padding: 10px;
  border-radius: 4px;
}

.log-item {
  font-family: monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #fff;
  margin-bottom: 4px;
}

.log-time {
  color: #888;
  margin-right: 8px;
}

.log-level {
  display: inline-block;
  padding: 0 4px;
  border-radius: 2px;
  margin-right: 8px;
  font-size: 12px;
}

.log-level.info {
  background-color: #409eff;
}

.log-level.error {
  background-color: #f56c6c;
}

.log-level.warning {
  background-color: #e6a23c;
}

.log-message {
  color: #fff;
}
</style> 