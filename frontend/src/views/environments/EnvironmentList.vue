<template>
  <div class="environment-list">
    <!-- 操作栏 -->
    <div class="operation-bar">
      <div class="left">
        <el-input
          v-model="searchQuery"
          placeholder="搜索环境名称"
          clearable
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="right">
        <el-button type="primary" @click="handleAdd">
          新增环境
        </el-button>
      </div>
    </div>

    <!-- 环境卡片列表 -->
    <div class="environment-cards" v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="8" v-for="env in environments" :key="env.id">
          <el-card class="environment-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="env-name">{{ env.name }}</span>
                <div class="card-actions">
                  <el-button type="primary" link @click="handleEdit(env)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button type="success" link @click="handleCopy(env)">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                  <el-button type="danger" link @click="handleDelete(env)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
            <div class="card-content">
              <div class="info-item">
                <span class="label">基础URL：</span>
                <el-tooltip
                  :content="env.base_url"
                  placement="top"
                  :show-after="500"
                >
                  <span class="value">{{ env.base_url }}</span>
                </el-tooltip>
              </div>
              <div class="info-item">
                <span class="label">变量数量：</span>
                <el-tag size="small" type="info">{{ env.variables_count }}个</el-tag>
              </div>
              <div class="info-item">
                <span class="label">创建时间：</span>
                <span class="value">{{ formatDate(env.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 空状态 -->
    <el-empty
      v-if="!loading && !environments.length"
      description="暂无环境配置"
    >
      <el-button type="primary" @click="handleAdd">新增环境</el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Edit,
  Delete,
  CopyDocument,
  Search
} from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const environments = ref([])

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 处理新增
const handleAdd = () => {
  router.push('/environments/create')
}

// 处理编辑
const handleEdit = (env: any) => {
  router.push(`/environments/${env.id}`)
}

// 处理复制
const handleCopy = (env: any) => {
  // TODO: 调用复制API
  ElMessage.success('复制成功')
}

// 处理删除
const handleDelete = (env: any) => {
  ElMessageBox.confirm(
    '确定要删除该环境配置吗？',
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

// 获取环境列表
const fetchEnvironments = () => {
  loading.value = true
  // TODO: 调用获取列表API
  // 模拟数据
  setTimeout(() => {
    environments.value = [
      {
        id: 1,
        name: '开发环境',
        base_url: 'http://dev-api.example.com',
        variables_count: 5,
        created_at: '2024-03-20 10:00:00'
      },
      {
        id: 2,
        name: '测试环境',
        base_url: 'http://test-api.example.com',
        variables_count: 3,
        created_at: '2024-03-20 11:00:00'
      },
      {
        id: 3,
        name: '预发环境',
        base_url: 'http://staging-api.example.com',
        variables_count: 4,
        created_at: '2024-03-20 12:00:00'
      }
    ]
    loading.value = false
  }, 500)
}

// 初始化
onMounted(() => {
  fetchEnvironments()
})
</script>

<style scoped>
.environment-list {
  height: 100%;
  padding: 20px;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.left {
  display: flex;
  align-items: center;
}

.right {
  display: flex;
  align-items: center;
}

.search-input {
  width: 300px;
}

.environment-cards {
  min-height: 200px;
}

.environment-card {
  margin-bottom: 20px;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.env-name {
  font-size: 16px;
  font-weight: bold;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  color: #909399;
  min-width: 80px;
}

.value {
  color: #303133;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style> 