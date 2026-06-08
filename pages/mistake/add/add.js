// pages/mistake/add/add.js
const app = getApp()

Page({
  data: {
    imagePath: '',
    recognizedText: '',
    questionText: '',
    correctAnswer: '',
    noteContent: '',
    
    // 学科固定为英语
    subjects: ['英语'],
    subjectIndex: 0,
    subjectId: 3, // 英语的学科ID
    subjectName: '英语',
    
    // 年级增加中考
    grades: ['初一', '初二', '初三', '中考'],
    gradeIndex: -1,
    gradeId: null,
    
    // 英语中考题型
    questionTypes: ['听力理解', '单项选择', '完形填空', '阅读理解', '词汇运用', '语法填空', '任务型阅读', '书面表达', '翻译', '其他'],
    typeIndex: -1,
    mistakeType: '',
    
    // 难度星级：0.5-5星，共10级
    difficultyLabels: ['半星', '1星', '1.5星', '2星', '2.5星', '3星', '3.5星', '4星', '4.5星', '5星'],
    difficultyLevels: [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
    difficultyIndex: 2, // 默认1.5星
    difficultyStars: '★☆',
    
    knowledgePoints: [],
    vocabulary: [],
    
    canSubmit: false
  },

  onLoad(options) {
    // 初始化难度星级显示
    this.setData({
      difficultyStars: this.generateStars(this.data.difficultyLevels[this.data.difficultyIndex])
    })
    
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

  // 年级选择
  onGradeChange(e) {
    const index = parseInt(e.detail.value)
    const gradeMap = {0: 1, 1: 2, 2: 3, 3: 4} // 初一=1, 初二=2, 初三=3, 中考=4
    this.setData({
      gradeIndex: index,
      gradeId: gradeMap[index]
    })
  },

  // 类型选择
  onTypeChange(e) {
    const index = parseInt(e.detail.value)
    const typeMap = {
      '听力理解': 'listening',
      '单项选择': 'choice',
      '完形填空': 'cloze',
      '阅读理解': 'reading',
      '词汇运用': 'vocabulary',
      '语法填空': 'grammar_blank',
      '任务型阅读': 'task_reading',
      '书面表达': 'writing',
      '翻译': 'translation',
      '其他': 'other'
    }
    this.setData({
      typeIndex: index,
      mistakeType: typeMap[this.data.questionTypes[index]]
    })
  },

  // 难度选择（星级）
  onDifficultyChange(e) {
    const index = parseInt(e.detail.value)
    const level = this.data.difficultyLevels[index]
    const stars = this.generateStars(level)
    this.setData({
      difficultyIndex: index,
      difficultyStars: stars,
      difficultyLevel: level
    })
  },
  
  // 生成星级显示
  generateStars(level) {
    const fullStars = Math.floor(level)
    const hasHalf = level % 1 !== 0
    let stars = '★'.repeat(fullStars)
    if (hasHalf) stars += '⯨' // 半星符号
    // 补齐空星
    const emptyStars = 5 - fullStars - (hasHalf ? 1 : 0)
    stars += '☆'.repeat(emptyStars)
    return stars
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
      difficulty: this.data.difficultyLevels[this.data.difficultyIndex], // 星级数值
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