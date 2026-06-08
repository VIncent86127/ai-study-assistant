// pages/mistake/detail/detail.js
const app = getApp()

// AI模型配置
const AI_MODELS = {
  deepseek: { name: 'DeepSeek V4', endpoint: '/api/ai/deepseek' },
  glm: { name: 'GLM', endpoint: '/api/ai/glm' }
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
    generating: false,
    deepseekQuestion: '',
    deepseekAnswer: '',
    glmQuestion: '',
    glmAnswer: '',
    
    // 做题状态
    showDoQuestionModal: false,
    currentDoingModel: '',
    currentQuestion: '',
    currentCorrectAnswer: '',
    userAnswer: '',
    showAnswer: false,
    
    // 结果状态
    showResultModal: false,
    reviewTime: '',
    reviewCount: 0,
    mastered: false
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
          // 为每个知识点添加expanded属性
          const knowledgePoints = (data.knowledge_points || []).map(kp => ({
            ...kp,
            expanded: false
          }))
          
          this.setData({
            mistake: data,
            knowledgePoints: knowledgePoints,
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

  // 切换知识点展开/折叠
  toggleKnowledge(e) {
    const index = e.currentTarget.dataset.index
    const knowledgePoints = this.data.knowledgePoints
    knowledgePoints[index].expanded = !knowledgePoints[index].expanded
    this.setData({ knowledgePoints })
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

  hideNoteModal() {
    this.setData({ showNoteModal: false })
  },

  stopPropagation() {},

  onNewNoteInput(e) {
    this.setData({ newNoteContent: e.detail.value })
  },

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

  editMistake() {
    wx.navigateTo({
      url: `/pages/mistake/add/add?id=${this.data.mistakeId}`
    })
  },

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
  
  generateSimilarQuestion() {
    this.setData({ 
      showGenerateModal: true,
      generating: true,
      deepseekQuestion: '',
      deepseekAnswer: '',
      glmQuestion: '',
      glmAnswer: ''
    })
    
    // 同时请求两个模型
    this.generateWithModel('deepseek')
    this.generateWithModel('glm')
  },
  
  hideGenerateModal() {
    this.setData({ showGenerateModal: false })
  },
  
  // 调用AI生成题目
  generateWithModel(model) {
    const { mistake, knowledgePoints } = this.data
    const knowledgeDesc = knowledgePoints.map(kp => kp.knowledge_content).join('、')
    
    wx.request({
      url: app.globalData.apiBase + '/api/ai/generate-question',
      method: 'POST',
      data: {
        model: model,
        original_question: mistake.question_text,
        correct_answer: mistake.correct_answer,
        knowledge_points: knowledgeDesc,
        question_type: mistake.mistake_type,
        difficulty: mistake.difficulty
      },
      success: (res) => {
        if (res.data.success) {
          if (model === 'deepseek') {
            this.setData({
              deepseekQuestion: res.data.data.question,
              deepseekAnswer: res.data.data.answer
            })
          } else if (model === 'glm') {
            this.setData({
              glmQuestion: res.data.data.question,
              glmAnswer: res.data.data.answer
            })
          }
          
          // 检查是否都生成完毕
          if (this.data.deepseekQuestion && this.data.glmQuestion) {
            this.setData({ generating: false })
          }
        }
      },
      fail: () => {
        this.setData({ generating: false })
        wx.showToast({ title: '生成失败', icon: 'none' })
      }
    })
  },
  
  // 开始做题
  doQuestion(e) {
    const model = e.currentTarget.dataset.model
    const question = model === 'deepseek' ? this.data.deepseekQuestion : this.data.glmQuestion
    const answer = model === 'deepseek' ? this.data.deepseekAnswer : this.data.glmAnswer
    
    this.setData({
      showGenerateModal: false,
      showDoQuestionModal: true,
      currentDoingModel: model,
      currentQuestion: question,
      currentCorrectAnswer: answer,
      userAnswer: '',
      showAnswer: false
    })
  },
  
  hideDoQuestionModal() {
    this.setData({ showDoQuestionModal: false })
  },
  
  onUserAnswerInput(e) {
    this.setData({ userAnswer: e.detail.value })
  },
  
  checkAnswer() {
    this.setData({ showAnswer: true })
  },
  
  markUnderstood() {
    this.saveReviewRecord(true)
  },
  
  markNotUnderstood() {
    this.saveReviewRecord(false)
  },
  
  // 保存复习记录
  saveReviewRecord(understood) {
    const { mistakeId, currentDoingModel, userAnswer } = this.data
    
    wx.request({
      url: app.globalData.apiBase + `/api/mistakes/${mistakeId}/review`,
      method: 'POST',
      data: {
        result: understood ? 'correct' : 'wrong',
        model: currentDoingModel,
        review_notes: userAnswer
      },
      success: (res) => {
        if (res.data.success) {
          const reviewCount = res.data.data.review_count || 1
          const mastered = res.data.data.mastered || false
          
          this.setData({
            showDoQuestionModal: false,
            showResultModal: true,
            reviewTime: new Date().toLocaleString(),
            reviewCount: reviewCount,
            mastered: mastered
          })
          
          // 重新加载错题详情
          this.loadMistakeDetail(mistakeId)
        }
      }
    })
  },
  
  hideResultModal() {
    this.setData({ showResultModal: false })
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