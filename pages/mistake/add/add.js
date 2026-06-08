// pages/mistake/add/add.js
const app = getApp()

Page({
  data: {
    imagePath: '',
    recognizedText: '',
    questionText: '',
    correctAnswer: '',
    noteContent: '',
    
    subjects: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'],
    subjectIndex: -1,
    subjectId: null,
    
    grades: ['初一', '初二', '初三'],
    gradeIndex: -1,
    gradeId: null,
    
    questionTypes: ['选择题', '填空题', '简答题', '计算题', '阅读理解', '作文'],
    typeIndex: -1,
    mistakeType: '',
    
    difficulties: ['简单', '中等', '困难'],
    difficultyIndex: 1,
    
    knowledgePoints: [],
    vocabulary: [],
    
    canSubmit: false
  },

  onLoad(options) {
    // 如果有传入图片路径
    if (options.imagePath) {
      this.setData({ imagePath: options.imagePath })
      this.recognizeImage(options.imagePath)
    }
  },

  // 选择图片
  chooseImage() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera', 'album'],
      success: (res) => {
        const imagePath = res.tempFiles[0].tempFilePath
        this.setData({ imagePath })
        this.recognizeImage(imagePath)
      }
    })
  },

  // 预览图片
  previewImage() {
    wx.previewImage({
      urls: [this.data.imagePath]
    })
  },

  // OCR识别
  recognizeImage(imagePath) {
    wx.showLoading({ title: '识别中...' })
    
    // 调用微信OCR API
    wx.serviceMarket.invokeService({
      service: 'wx79ac3de8be320b71',
      api: 'OcrAll',
      data: {
        img_url: imagePath
      }
    }).then(res => {
      wx.hideLoading()
      
      if (res.data && res.data.text) {
        const recognizedText = res.data.text
        this.setData({ 
          recognizedText,
          questionText: recognizedText
        })
        
        // 自动分析题目
        if (this.data.subjectId) {
          this.analyzeQuestion()
        }
      }
    }).catch(err => {
      wx.hideLoading()
      console.error('OCR识别失败', err)
      
      // 模拟识别结果（开发阶段）
      this.setData({
        recognizedText: '示例题目内容（OCR识别失败）',
        questionText: '示例题目内容（OCR识别失败）'
      })
    })
  },

  // 分析题目
  analyzeQuestion() {
    const { questionText, subjectId } = this.data
    if (!questionText || !subjectId) return
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes/analyze',
      method: 'POST',
      data: {
        question_text: questionText,
        subject_id: subjectId
      },
      success: (res) => {
        if (res.data.success) {
          this.setData({
            knowledgePoints: res.data.data.knowledge_points,
            vocabulary: res.data.data.vocabulary
          })
        }
      }
    })
  },

  // 编辑题目文本
  editQuestionText() {
    this.setData({
      editingQuestion: true
    })
  },

  onQuestionInput(e) {
    this.setData({ questionText: e.detail.value })
    this.checkCanSubmit()
  },

  onAnswerInput(e) {
    this.setData({ correctAnswer: e.detail.value })
    this.checkCanSubmit()
  },

  onNoteInput(e) {
    this.setData({ noteContent: e.detail.value })
  },

  // 学科选择
  onSubjectChange(e) {
    const index = parseInt(e.detail.value)
    const subjectName = this.data.subjects[index]
    
    // 获取学科ID
    wx.request({
      url: app.globalData.apiBase + '/api/subjects/list',
      success: (res) => {
        // 简化处理，假设按顺序
        this.setData({
          subjectIndex: index,
          subjectId: index + 1  // 实际应该从API获取
        })
        
        // 如果已有题目文本，重新分析
        if (this.data.questionText) {
          this.analyzeQuestion()
        }
      }
    })
  },

  // 年级选择
  onGradeChange(e) {
    const index = parseInt(e.detail.value)
    this.setData({
      gradeIndex: index,
      gradeId: index + 1  // 实际应该从API获取
    })
  },

  // 类型选择
  onTypeChange(e) {
    const index = parseInt(e.detail.value)
    const types = ['choice', 'blank', 'short', 'calculation', 'reading', 'composition']
    this.setData({
      typeIndex: index,
      mistakeType: types[index]
    })
  },

  // 难度选择
  onDifficultyChange(e) {
    const index = parseInt(e.detail.value)
    const diffMap = ['easy', 'medium', 'hard']
    this.setData({
      difficultyIndex: index
    })
  },

  // 检查是否可以提交
  checkCanSubmit() {
    const { questionText, correctAnswer, subjectIndex } = this.data
    this.setData({
      canSubmit: questionText.length > 0 && subjectIndex >= 0
    })
  },

  // 语音输入
  startVoiceRecord() {
    wx.showModal({
      title: '语音输入',
      content: '请开始说话，系统将自动识别您的语音并转换为文字',
      success: (res) => {
        if (res.confirm) {
          // 开始录音
          wx.startRecord({
            success: (res) => {
              const tempFilePath = res.tempFilePath
              // 语音识别（需要调用语音识别API）
              this.recognizeVoice(tempFilePath)
            },
            fail: (err) => {
              wx.showToast({ title: '录音失败', icon: 'none' })
            }
          })
        }
      }
    })
  },

  // 语音识别
  recognizeVoice(filePath) {
    wx.showLoading({ title: '识别中...' })
    
    // 调用语音识别API
    // 实际项目中需要使用腾讯云或百度语音识别服务
    setTimeout(() => {
      wx.hideLoading()
      const mockText = '这是语音识别的示例文本（实际需要调用API）'
      
      this.setData({
        noteContent: this.data.noteContent + '\n' + mockText
      })
      
      wx.showToast({ title: '识别成功', icon: 'success' })
    }, 1000)
  },

  // 提交错题
  submitMistake() {
    if (!this.data.canSubmit) return
    
    const data = {
      user_id: app.globalData.userId || 'default',
      subject_id: this.data.subjectId,
      grade_id: this.data.gradeId,
      question_text: this.data.questionText,
      correct_answer: this.data.correctAnswer,
      mistake_type: this.data.mistakeType || 'unknown',
      difficulty: ['easy', 'medium', 'hard'][this.data.difficultyIndex],
      knowledge_points: this.data.knowledgePoints.map(kp => ({
        type: kp.type,
        id: kp.id
      })),
      vocabulary: this.data.vocabulary,
      notes: this.data.noteContent ? [{
        type: 'text',
        content: this.data.noteContent
      }] : []
    }
    
    wx.showLoading({ title: '保存中...' })
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes',
      method: 'POST',
      data: data,
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          wx.showToast({ title: '保存成功', icon: 'success' })
          
          setTimeout(() => {
            wx.navigateBack()
          }, 1500)
        } else {
          wx.showToast({ title: '保存失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  }
})