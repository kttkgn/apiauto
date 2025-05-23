<template>
  <div class="report-detail">
    <!-- 基本信息 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
          <el-button type="primary" @click="handleDownload">
            下载报告
          </el-button>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="报告名称">{{ reportInfo.name }}</el-descriptions-item>
        <el-descriptions-item label="执行环境">{{ reportInfo.environment }}</el-descriptions-item>
        <el-descriptions-item label="执行时间">{{ reportInfo.created_at }}</el-descriptions-item>
        <el-descriptions-item label="执行人">{{ reportInfo.executor }}</el-descriptions-item>
        <el-descriptions-item label="执行范围">
          <el-tag :type="getScopeType(reportInfo.scope)">{{ getScopeLabel(reportInfo.scope) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="执行时长">{{ reportInfo.duration }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 执行结果概览 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>执行结果概览</span>
        </div>
      </template>
      <div class="overview">
        <div class="overview-item">
          <div class="value">{{ reportInfo.total_cases }}</div>
          <div class="label">总用例数</div>
        </div>
        <div class="overview-item">
          <div class="value success">{{ reportInfo.passed_cases }}</div>
          <div class="label">通过用例</div>
        </div>
        <div class="overview-item">
          <div class="value danger">{{ reportInfo.failed_cases }}</div>
          <div class="label">失败用例</div>
        </div>
        <div class="overview-item">
          <div class="value">{{ reportInfo.pass_rate }}%</div>
          <div class="label">通过率</div>
        </div>
      </div>
    </el-card>

    <!-- 用例执行结果 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>用例执行结果</span>
          <div class="header-right">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用例"
              clearable
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select v-model="statusFilter" placeholder="状态筛选">
              <el-option label="全部" value="" />
              <el-option label="通过" value="success" />
              <el-option label="失败" value="failed" />
            </el-select>
          </div>
        </div>
      </template>
      <el-table :data="filteredCaseResults" style="width: 100%">
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
        <el-table-column prop="duration" label="执行时长" width="120" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')

// 报告信息
const reportInfo = ref({
  name: '',
  environment: '',
  created_at: '',
  executor: '',
  scope: '',
  duration: '',
  total_cases: 0,
  passed_cases: 0,
  failed_cases: 0,
  pass_rate: 0
})

// 用例执行结果
const caseResults = ref([
  {
    id: 1,
    name: '用户登录接口测试',
    api_name: 'POST /api/login',
    status: 'success',
    duration: '1.2s',
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
    duration: '0.8s',
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

// 过滤后的用例结果
const filteredCaseResults = computed(() => {
  return caseResults.value.filter(item => {
    const matchSearch = !searchQuery.value || 
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.api_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = !statusFilter.value || item.status === statusFilter.value
    return matchSearch && matchStatus
  })
})

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
    success: '通过',
    failed: '失败'
  }
  return map[status] || status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    success: 'success',
    failed: 'danger'
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

// 下载报告
const handleDownload = () => {
  // TODO: 调用下载API
  ElMessage.success('开始下载报告')
}

// 获取报告详情
const fetchReportDetail = (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  Object.assign(reportInfo, {
    name: '用户模块测试报告',
    environment: '开发环境',
    created_at: '2024-03-20 10:00:00',
    executor: '张三',
    scope: 'module',
    duration: '00:01:30',
    total_cases: 10,
    passed_cases: 8,
    failed_cases: 2,
    pass_rate: 80
  })
}

// 初始化
onMounted(() => {
  const id = route.params.id
  if (id) {
    fetchReportDetail(id as string)
  }
})
</script>

<style scoped>
.report-detail {
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

.header-right {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 200px;
}

.overview {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.overview-item {
  text-align: center;
}

.overview-item .value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.overview-item .value.success {
  color: #67c23a;
}

.overview-item .value.danger {
  color: #f56c6c;
}

.overview-item .label {
  color: #606266;
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

.json-content {
  margin: 0;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}
</style> 