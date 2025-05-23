<template>
  <div class="case-list">
    <!-- 顶部操作栏 -->
    <div class="operation-bar">
      <div class="left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>新增用例
        </el-button>
        <el-button type="danger" :disabled="!selectedCases.length" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>批量删除
        </el-button>
        <el-button type="success" :disabled="!selectedCases.length" @click="handleBatchExecute">
          <el-icon><VideoPlay /></el-icon>批量执行
        </el-button>
      </div>
      <div class="right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用例名称或模块"
          class="search-input"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 用例列表表格 -->
    <el-table
      v-loading="loading"
      :data="tableData"
      @selection-change="handleSelectionChange"
      border
      style="width: 100%"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="name" label="用例名称" min-width="150" show-overflow-tooltip />
      <el-table-column prop="module" label="所属模块" width="120" />
      <el-table-column prop="method" label="请求方法" width="100">
        <template #default="{ row }">
          <el-tag :type="getMethodTagType(row.method)">{{ row.method }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="path" label="请求路径" min-width="200" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" link @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>编辑
            </el-button>
            <el-button type="success" link @click="handleExecute(row)">
              <el-icon><VideoPlay /></el-icon>执行
            </el-button>
            <el-button type="danger" link @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <div class="pagination-container">
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Delete,
  VideoPlay,
  Search,
  Edit
} from '@element-plus/icons-vue'

// 路由
const router = useRouter()

// 表格数据
const loading = ref(false)
const tableData = ref([])
const selectedCases = ref([])
const searchQuery = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 获取方法标签类型
const getMethodTagType = (method: string) => {
  const types: Record<string, string> = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger'
  }
  return types[method] || 'info'
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 处理选择变化
const handleSelectionChange = (selection: any[]) => {
  selectedCases.value = selection
}

// 处理新增
const handleAdd = () => {
  router.push('/cases/create')
}

// 处理编辑
const handleEdit = (row: any) => {
  router.push(`/cases/${row.id}`)
}

// 处理删除
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该用例吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用删除API
    ElMessage.success('删除成功')
  })
}

// 处理批量删除
const handleBatchDelete = () => {
  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedCases.value.length} 个用例吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用批量删除API
    ElMessage.success('批量删除成功')
  })
}

// 处理执行
const handleExecute = (row: any) => {
  // TODO: 调用执行API
  ElMessage.success('开始执行用例')
}

// 处理批量执行
const handleBatchExecute = () => {
  // TODO: 调用批量执行API
  ElMessage.success('开始批量执行用例')
}

// 处理分页大小变化
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

// 处理页码变化
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchData()
}

// 获取数据
const fetchData = () => {
  loading.value = true
  // TODO: 调用获取列表API
  // 模拟数据
  setTimeout(() => {
    tableData.value = [
      {
        id: 1,
        name: '测试用例1',
        module: '用户模块',
        method: 'GET',
        path: '/api/v1/users',
        created_at: '2024-03-20 10:00:00'
      },
      {
        id: 2,
        name: '测试用例2',
        module: '订单模块',
        method: 'POST',
        path: '/api/v1/orders',
        created_at: '2024-03-20 11:00:00'
      }
    ]
    total.value = 100
    loading.value = false
  }, 500)
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.case-list {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.operation-bar {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 8px;
}

.search-input {
  width: 300px;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-table) {
  flex: 1;
  margin-bottom: 16px;
}
</style> 