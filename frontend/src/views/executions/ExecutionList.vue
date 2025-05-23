<template>
  <div class="execution-list">
    <!-- 顶部操作栏 -->
    <div class="operation-bar">
      <div class="left">
        <el-input
          v-model="searchQuery"
          placeholder="请输入用例名称"
          clearable
          @keyup.enter="handleSearch"
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="statusFilter" placeholder="执行状态" @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="成功" value="success" />
          <el-option label="失败" value="failed" />
          <el-option label="执行中" value="running" />
        </el-select>
      </div>
      <div class="right">
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>刷新
        </el-button>
        <el-button type="primary" @click="handleNewExecution">
          <el-icon><Plus /></el-icon>新增执行
        </el-button>
      </div>
    </div>

    <!-- 执行记录列表 -->
    <el-table
      v-loading="loading"
      :data="executionList"
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="用例名称" min-width="200">
        <template #default="{ row }">
          <el-tooltip :content="row.name" placement="top" :show-after="500">
            <span class="ellipsis">{{ row.name }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="scope" label="执行范围" width="120">
        <template #default="{ row }">
          <el-tag :type="getScopeType(row.scope)">{{ getScopeLabel(row.scope) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="environment" label="环境" width="120">
        <template #default="{ row }">
          <el-tag>{{ row.environment }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="parameters" label="执行参数" min-width="200">
        <template #default="{ row }">
          <el-tooltip :content="formatParameters(row.parameters)" placement="top" :show-after="500">
            <span class="ellipsis">{{ formatParameters(row.parameters) }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="executor" label="执行人" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="执行时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button 
            type="primary" 
            link 
            @click="handleViewDetail(row)"
            :disabled="row.status === 'failed'"
          >
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增执行对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新增执行"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="执行范围" prop="scope">
          <el-select v-model="formData.scope" placeholder="请选择执行范围">
            <el-option label="单个用例" value="single" />
            <el-option label="模块用例" value="module" />
            <el-option label="全部用例" value="all" />
          </el-select>
        </el-form-item>
        <el-form-item label="环境" prop="environment">
          <el-select v-model="formData.environment" placeholder="请选择环境">
            <el-option
              v-for="env in environments"
              :key="env.id"
              :label="env.name"
              :value="env.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="执行参数" prop="parameters">
          <el-input
            v-model="formData.parameters"
            type="textarea"
            :rows="3"
            placeholder="请输入执行参数（JSON格式）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 表单数据
const formData = reactive({
  scope: '',
  environment: '',
  parameters: ''
})

// 表单验证规则
const rules: FormRules = {
  scope: [{ required: true, message: '请选择执行范围', trigger: 'change' }],
  environment: [{ required: true, message: '请选择环境', trigger: 'change' }]
}

// 环境列表（模拟数据）
const environments = ref([
  { id: 1, name: '开发环境' },
  { id: 2, name: '测试环境' },
  { id: 3, name: '生产环境' }
])

// 执行列表（模拟数据）
const executionList = ref([
  {
    id: 1,
    name: '用户登录接口测试',
    scope: 'single',
    environment: '开发环境',
    parameters: { userId: 123, token: 'xxx' },
    executor: '张三',
    status: 'success',
    created_at: '2024-03-20 10:00:00'
  },
  {
    id: 2,
    name: '订单模块测试',
    scope: 'module',
    environment: '测试环境',
    parameters: { orderId: 456 },
    executor: '李四',
    status: 'running',
    created_at: '2024-03-20 11:00:00'
  }
])

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

// 格式化参数
const formatParameters = (parameters: any) => {
  try {
    return JSON.stringify(parameters)
  } catch {
    return parameters
  }
}

// 格式化日期
const formatDate = (date: string) => {
  return date
}

// 搜索
const handleSearch = () => {
  // TODO: 调用搜索API
  console.log('搜索:', searchQuery.value, statusFilter.value)
}

// 刷新
const handleRefresh = () => {
  // TODO: 调用刷新API
  console.log('刷新')
}

// 新增执行
const handleNewExecution = () => {
  router.push('/executions/config')
}

// 查看执行详情
const handleViewDetail = (row: any) => {
  router.push({
    path: `/executions/${row.id}`,
    query: {
      scope: row.scope
    }
  })
}

// 行点击
const handleRowClick = (row: any) => {
  handleViewDetail(row)
}

// 分页大小改变
const handleSizeChange = (val: number) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

// 页码改变
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用提交API
      ElMessage.success('创建成功')
      dialogVisible.value = false
    }
  })
}

// 编辑执行
const handleEdit = (row: any) => {
  router.push(`/executions/config?id=${row.id}`)
}

// 初始化
onMounted(() => {
  // TODO: 加载初始数据
})
</script>

<style scoped>
.execution-list {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.operation-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.right {
  display: flex;
  gap: 16px;
}

.ellipsis {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 