<template>
  <div class="module-form">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑模块' : '新增模块' }}</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <!-- 基本信息 -->
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

        <!-- 局部变量配置 -->
        <el-form-item label="局部变量">
          <div class="variables-header">
            <el-button type="primary" @click="handleAddVariable">
              添加变量
            </el-button>
          </div>
          <el-table :data="formData.variables" style="width: 100%">
            <el-table-column label="变量名" min-width="150">
              <template #default="{ row }">
                <el-input v-model="row.name" placeholder="变量名" />
              </template>
            </el-table-column>
            <el-table-column label="变量值" min-width="200">
              <template #default="{ row }">
                <el-input v-model="row.value" placeholder="变量值" />
              </template>
            </el-table-column>
            <el-table-column label="描述" min-width="200">
              <template #default="{ row }">
                <el-input v-model="row.description" placeholder="描述" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ $index }">
                <el-button
                  type="primary"
                  link
                  @click="handleExtractor($index)"
                >
                  提取器设置
                </el-button>
                <el-button
                  type="danger"
                  link
                  @click="handleRemoveVariable($index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>

        <!-- 表单操作按钮 -->
        <el-form-item>
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 变量提取器 -->
    <variable-extractor
      v-if="extractorVisible"
      v-model="currentVariable"
      @save="handleExtractorSave"
      @cancel="extractorVisible = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import VariableExtractor from '../../components/VariableExtractor.vue'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 判断是否为编辑模式
const isEdit = ref(false)

// 提取器相关
const extractorVisible = ref(false)
const currentVariable = ref({
  name: '',
  value: '',
  description: '',
  extractor: {
    source: 'response_body',
    method: 'jsonpath',
    expression: '',
    test_url: '',
    test_method: 'GET',
    test_headers: [],
    test_params: [],
    test_body: ''
  }
})
const currentVariableIndex = ref(-1)

// 表单数据
const formData = ref({
  id: '',
  name: '',
  description: '',
  variables: [] as Array<{
    name: string
    value: string
    description: string
  }>
})

// 表单验证规则
const rules: FormRules = {
  name: [{ required: true, message: '请输入模块名称', trigger: 'blur' }]
}

// 添加变量
const handleAddVariable = () => {
  formData.value.variables.push({
    name: '',
    value: '',
    description: ''
  })
}

// 删除变量
const handleRemoveVariable = (index: number) => {
  formData.value.variables.splice(index, 1)
}

// 提取器设置
const handleExtractor = (index: number) => {
  currentVariableIndex.value = index
  currentVariable.value = {
    ...formData.value.variables[index],
    extractor: {
      source: 'response_body',
      method: 'jsonpath',
      expression: '',
      test_url: '',
      test_method: 'GET',
      test_headers: [],
      test_params: [],
      test_body: ''
    }
  }
  extractorVisible.value = true
}

// 保存提取器设置
const handleExtractorSave = (variable: any) => {
  if (currentVariableIndex.value > -1) {
    formData.value.variables[currentVariableIndex.value] = {
      ...variable,
      value: variable.extractor.expression
    }
  }
  extractorVisible.value = false
}

// 取消
const handleCancel = () => {
  router.back()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用保存API
      ElMessage.success(isEdit.value ? '编辑成功' : '新增成功')
      router.back()
    }
  })
}

// 获取模块详情
const fetchModuleDetail = async (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  formData.value = {
    id,
    name: '用户模块',
    description: '用户相关的接口测试用例',
    variables: [
      {
        name: 'base_url',
        value: 'http://api.example.com',
        description: '接口基础地址'
      },
      {
        name: 'token',
        value: '${token}',
        description: '认证令牌'
      }
    ]
  }
}

// 初始化
onMounted(() => {
  const id = route.query.id as string
  if (id) {
    isEdit.value = true
    fetchModuleDetail(id)
  }
})
</script>

<style scoped>
.module-form {
  height: 100%;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.variables-header {
  margin-bottom: 16px;
}

:deep(.el-form-item__content) {
  justify-content: flex-start;
}
</style> 