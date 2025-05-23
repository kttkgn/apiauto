<template>
  <el-dialog
    v-model="dialogVisible"
    title="变量提取器设置"
    width="800px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <!-- 提取规则配置 -->
      <el-form-item label="来源" prop="source">
        <el-radio-group v-model="formData.source">
          <el-radio label="response_header">响应头</el-radio>
          <el-radio label="response_body">响应体</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="提取方式" prop="extract_type">
        <el-radio-group v-model="formData.extract_type">
          <el-radio label="jsonpath">JSONPath</el-radio>
          <el-radio label="regex">正则表达式</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="提取表达式" prop="expression">
        <el-input
          v-model="formData.expression"
          :placeholder="getExpressionPlaceholder"
          type="textarea"
          :rows="3"
        />
      </el-form-item>

      <!-- 测试区域 -->
      <el-form-item label="测试数据">
        <el-input
          v-model="testData"
          type="textarea"
          :rows="5"
          placeholder="请输入测试数据"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleTest">
          测试提取
        </el-button>
      </el-form-item>

      <el-form-item v-if="testResult" label="提取结果">
        <el-alert
          :title="testResult"
          :type="testSuccess ? 'success' : 'error'"
          :closable="false"
          show-icon
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">
          保存
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const props = defineProps<{
  modelValue: boolean
  variable: {
    name: string
    value: string
    description: string
  }
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', data: any): void
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formRef = ref<FormInstance>()
const testData = ref('')
const testResult = ref('')
const testSuccess = ref(false)

// 表单数据
const formData = ref({
  source: 'response_body',
  extract_type: 'jsonpath',
  expression: ''
})

// 表单验证规则
const rules: FormRules = {
  source: [{ required: true, message: '请选择来源', trigger: 'change' }],
  extract_type: [{ required: true, message: '请选择提取方式', trigger: 'change' }],
  expression: [{ required: true, message: '请输入提取表达式', trigger: 'blur' }]
}

// 获取表达式占位符
const getExpressionPlaceholder = computed(() => {
  if (formData.value.extract_type === 'jsonpath') {
    return '请输入JSONPath表达式，例如：$.data.token'
  }
  return '请输入正则表达式，例如：(?<=token=)[^&]+'
})

// 监听提取方式变化
watch(() => formData.value.extract_type, () => {
  formData.value.expression = ''
})

// 测试提取
const handleTest = () => {
  if (!testData.value) {
    ElMessage.warning('请输入测试数据')
    return
  }

  try {
    if (formData.value.extract_type === 'jsonpath') {
      // TODO: 实现JSONPath提取
      testResult.value = '提取成功：xxx'
      testSuccess.value = true
    } else {
      // TODO: 实现正则提取
      testResult.value = '提取成功：xxx'
      testSuccess.value = true
    }
  } catch (error) {
    testResult.value = '提取失败：' + (error as Error).message
    testSuccess.value = false
  }
}

// 取消
const handleCancel = () => {
  dialogVisible.value = false
  resetForm()
}

// 保存
const handleSave = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('save', {
        ...formData.value,
        variable_name: props.variable.name
      })
      dialogVisible.value = false
      resetForm()
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  testData.value = ''
  testResult.value = ''
  testSuccess.value = false
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}
</style> 