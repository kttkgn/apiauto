<template>
  <div class="module-list">
    <!-- 操作栏 -->
    <div class="operation-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索模块名称"
        clearable
        class="search-input"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-button type="primary" @click="handleAdd">
        新增模块
      </el-button>
    </div>

    <!-- 模块列表 -->
    <el-table :data="filteredModules" style="width: 100%" v-loading="loading">
      <el-table-column prop="name" label="模块名称" min-width="200" />
      <el-table-column prop="description" label="描述" min-width="300" />
      <el-table-column prop="case_count" label="用例数量" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button type="danger" link @click="handleDelete(row)">
            删除
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
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 模块表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑模块' : '新增模块'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="模块名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入模块名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入模块描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 搜索和分页
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const formData = ref({
  id: '',
  name: '',
  description: ''
})

// 表单验证规则
const rules: FormRules = {
  name: [{ required: true, message: '请输入模块名称', trigger: 'blur' }]
}

// 模块列表数据
const modules = ref([
  {
    id: '1',
    name: '用户模块',
    description: '用户相关的接口测试用例',
    case_count: 10,
    created_at: '2024-03-20 10:00:00',
    updated_at: '2024-03-20 10:00:00'
  },
  {
    id: '2',
    name: '订单模块',
    description: '订单相关的接口测试用例',
    case_count: 8,
    created_at: '2024-03-20 11:00:00',
    updated_at: '2024-03-20 11:00:00'
  }
])

// 过滤后的模块列表
const filteredModules = computed(() => {
  return modules.value.filter(item =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 新增模块
const handleAdd = () => {
  router.push('/modules/form')
}

// 编辑模块
const handleEdit = (row: any) => {
  router.push({
    path: '/modules/form',
    query: { id: row.id }
  })
}

// 删除模块
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该模块吗？删除后不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用删除API
    const index = modules.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      modules.value.splice(index, 1)
    }
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      if (isEdit.value) {
        // TODO: 调用编辑API
        const index = modules.value.findIndex(item => item.id === formData.value.id)
        if (index > -1) {
          modules.value[index] = {
            ...modules.value[index],
            ...formData.value,
            updated_at: new Date().toLocaleString()
          }
        }
        ElMessage.success('编辑成功')
      } else {
        // TODO: 调用新增API
        modules.value.push({
          ...formData.value,
          id: Date.now().toString(),
          case_count: 0,
          created_at: new Date().toLocaleString(),
          updated_at: new Date().toLocaleString()
        })
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
    }
  })
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

// 初始化
onMounted(() => {
  // TODO: 加载模块列表数据
})
</script>

<style scoped>
.module-list {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}
</style> 