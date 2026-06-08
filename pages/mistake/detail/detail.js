// pages/mistake/detail/detail.js
const app = getApp()

// AI模型配置
const AI_MODELS = {
  gpt: { name: 'GPT-4', endpoint: '/api/ai/gpt' },
  claude: { name: 'Claude', endpoint: '/api/ai/claude' },
  glm: { name: '智谱GLM', endpoint: '/api/ai/glm' },
  qwen: { name: '通义千问', endpoint: '/api/ai/qwen' },
  deepseek: { name: 'DeepSeek V4', endpoint: '/api/ai/deepseek' },
  openmaic: { name: 'OpenMAIC', endpoint: '/api/ai/openmaic' }
}

Page({
  data: {
    mistakeId: null,
    mistake: {},
    knowledgePoints: [],
    vocabulary: [],
    notes: [],
    reviewHistory: [],
    
    showNoteModal: false,
    newNoteContent: '',
    
    // AI生成相关
    showGenerateModal: false,
    currentModel: 'deepseek',  // 默认使用DeepSeek
    currentModelName: 'DeepSeek V4',
    generating: false,
    generatedQuestion: '',
    generatedAnswer: ''
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ mistakeId: options.id })
      this.loadMistakeDetail(options.id)
    }
  },

  // 加载错题详情
  loadMistakeDetail(id) {
    wx.showLoading({ title: '加载中...' })
    
    wx.request({
      url: app.globalData.apiBase + `/api/mistakes/${id}`,
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          const data = res.data.data
          this.setData({
            mistake: data,
            knowledgePoints: data.knowledge_points || [],
            vocabulary: data.vocabulary || [],
            notes: data.notes || [],
            reviewHistory: data.review_history || []
          })
        } else {
          wx.showToast({ title: '加载失败', icon: 'none' })
        }
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  },

  // 跳转到知识点详情
  goToKnowledge(e) {
    const item = e.currentTarget.dataset.item
    wx.navigateTo({
      url: `/pages/subject/subject?type=${item.knowledge_type}&id=${item.knowledge_id}`
    })
  },

  // 显示添加备注弹窗
  addNote() {
    this.setData({ 
      showNoteModal: true,
      newNoteContent: ''
    })
  },

  // 隐藏弹窗
  hideNoteModal() {
    this.setData({ showNoteModal: false })
  },

  // 阻止冒泡
  stopPropagation() {},

  // 输入备注
  onNewNoteInput(e) {
    this.setData({ newNoteContent: e.detail.value })
  },

  // 提交备注
  submitNote() {
    const content = this.data.newNoteContent.trim()
    if (!content) {
      wx.showToast({ title: '请输入内容', icon: 'none' })
      return
    }
    
    wx.request({
      url: app.globalData.apiBase + `/api/mistakes/${this.data.mistakeId}/notes`,
      method: 'POST',
      data: {
        type: 'text',
        content: content
      },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ title: '添加成功', icon: 'success' })
          this.setData({ showNoteModal: false })
          this.loadMistakeDetail(this.data.mistakeId)
        }
      }
    })
  },

  // 开始复习
  startReview() {
    wx.showModal({
      title: '复习结果',
      content: '请选择本次复习的结果',
      showCancel: true,
      cancelText: '错误',
      confirmText: '正确',
      success: (res) => {
        const result = res.confirm ? 'correct' : 'wrong'
        this.submitReview(result)
      }
    })
  },

  // 提交复习记录
  submitReview(result) {
    wx.request({
      url: app.globalData.apiBase + `/api/mistakes/${this.data.mistakeId}/review`,
      method: 'POST',
      data: { result },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ 
            title: result === 'correct' ? '答对了！' : '继续加油！', 
            icon: 'success' 
          })
          this.loadMistakeDetail(this.data.mistakeId)
        }
      }
    })
  },

  // 编辑错题
  editMistake() {
    wx.navigateTo({
      url: `/pages/mistake/add/add?id=${this.data.mistakeId}`
    })
  },

  // 删除错题
  deleteMistake() {
    wx.showModal({
      title: '确认删除',
      content: '删除后无法恢复，确定要删除吗？',
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: app.globalData.apiBase + `/api/mistakes/${this.data.mistakeId}`,
            method: 'DELETE',
            success: (res) => {
              if (res.data.success) {
                wx.showToast({ title: '已删除', icon: 'success' })
                setTimeout(() => {
                  wx.navigateBack()
                }, 1500)
              }
            }
          })
        }
      }
    })
  },

  // ========== AI生成类似题目功能 ==========
  
  // 显示生成弹窗
  generateSimilarQuestion() {
    this.setData({ 
      showGenerateModal: true,
      generatedQuestion: '',
      generatedAnswer: '',
      generating: false
    })
  },
  
  // 隐藏生成弹窗
  hideGenerateModal() {
    this.setData({ showGenerateModal: false })
  },
  
  // 选择AI模型
  selectModel(e) {
    const model = e.currentTarget.dataset.model
    this.setData({
      currentModel: model,
      currentModelName: AI_MODELS[model].name,
      generatedQuestion: '',
      generatedAnswer: ''
    })
  },
  
  // 开始生成
  startGenerate() {
    this.generateQuestion()
  },
  
  // 重新生成
  regenerateQuestion() {
    this.generateQuestion()
  },
  
  // 调用AI生成题目
  generateQuestion() {
    const { mistake, knowledgePoints, currentModel } = this.data
    
    this.setData({ generating: true })
    
    // 构建知识点描述
    const knowledgeDesc = knowledgePoints.map(kp => kp.knowledge_content).join('、')
    
    // 调用后端API生成题目
    wx.request({
      url: app.globalData.apiBase + '/api/ai/generate-question',
      method: 'POST',
      data: {
        model: currentModel,
        original_question: mistake.question_text,
        correct_answer: mistake.correct_answer,
        knowledge_points: knowledgeDesc,
        question_type: mistake.mistake_type,
        difficulty: mistake.difficulty
      },
      success: (res) => {
        this.setData({ generating: false })
        
        if (res.data.success) {
          this.setData({
            generatedQuestion: res.data.data.question,
            generatedAnswer: res.data.data.answer
          })
        } else {
          wx.showToast({ title: '生成失败，请重试', icon: 'none' })
        }
      },
      fail: () => {
        this.setData({ generating: false })
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  },
  
  // 保存生成的题目到错题本
  saveGeneratedQuestion() {
    const { generatedQuestion, generatedAnswer, mistake } = this.data
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes',
      method: 'POST',
      data: {
        user_id: app.globalData.userId || 'test_user',
        subject_id: mistake.subject_id,
        grade_id: mistake.grade_id,
        question_text: generatedQuestion,
        correct_answer: generatedAnswer,
        mistake_type: mistake.mistake_type,
        difficulty: mistake.difficulty,
        notes: [{
          type: 'text',
          content: 'AI生成的类似题目'
        }]
      },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ title: '已加入错题本', icon: 'success' })
          this.hideGenerateModal()
        }
      }
    })
  },
  
  // 重新分析知识点
  analyzeAgain() {
    wx.showLoading({ title: '分析中...' })
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes/analyze',
      method: 'POST',
      data: {
        question_text: this.data.mistake.question_text,
        subject_id: this.data.mistake.subject_id
      },
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          // 更新知识点
          const newKnowledge = res.data.data.knowledge_points
          this.setData({ knowledgePoints: newKnowledge })
          wx.showToast({ title: '分析完成', icon: 'success' })
        }
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '分析失败', icon: 'none' })
      }
    })
  }
})