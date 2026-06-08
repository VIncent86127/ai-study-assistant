// pages/mistake/add/add.js
const app = getApp()

Page({
  data: {
    imagePath: '',
    recognizedText: '',
    questionText: '',
    correctAnswer: '',
    noteContent: '',
    
    // 学科选择
    subjects: ['英语', '数学'],
    subjectIndex: 0,
    subjectId: 3, // 英语的学科ID
    subjectName: '英语',
    
    // 年级增加中考
    grades: ['初一', '初二', '初三', '中考'],
    gradeIndex: -1,
    gradeId: null,
    
    // 英语中考题型
    englishQuestionTypes: ['听力理解', '单项选择', '完形填空', '阅读理解', '词汇运用', '语法填空', '任务型阅读', '书面表达', '翻译', '其他'],
    // 数学中考题型
    mathQuestionTypes: ['选择题', '填空题', '计算题', '证明题', '应用题', '综合题', '解答题', '探究题', '其他'],
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
      // 如果OCR失败，手动输入
      this.setData({
        questionText: ''
      })
    })
  },

  // 选择学科
  onSubjectChange(e) {
    const index = parseInt(e.detail.value)
    const subjectMap = {
      0: { id: 3, name: '英语' },  // 英语的ID
      1: { id: 2, name: '数学' }   // 数学的ID
    }
    
    const subject = subjectMap[index]
    const questionTypes = index === 0 ? this.data.englishQuestionTypes : this.data.mathQuestionTypes
    
    this.setData({
      subjectIndex: index,
      subjectId: subject.id,
      subjectName: subject.name,
      questionTypes: questionTypes,
      typeIndex: -1,
      mistakeType: ''
    })
    
    // 重新分析题目
    if (this.data.questionText) {
      this.analyzeQuestion()
    }
  },

  // 选择年级
  onGradeChange(e) {
    const index = parseInt(e.detail.value)
    const gradeMap = { 0: 1, 1: 2, 2: 3, 3: 4 } // 初一、初二、初三、中考
    
    this.setData({
      gradeIndex: index,
      gradeId: gradeMap[index]
    })
  },

  // 选择题型
  onTypeChange(e) {
    const index = parseInt(e.detail.value)
    this.setData({
      typeIndex: index,
      mistakeType: this.data.questionTypes[index]
    })
  },

  // 选择难度
  onDifficultyChange(e) {
    const index = parseInt(e.detail.value)
    this.setData({
      difficultyIndex: index,
      difficultyStars: this.generateStars(this.data.difficultyLevels[index])
    })
  },

  // 生成星级显示
  generateStars(level) {
    const fullStars = Math.floor(level)
    const hasHalf = level % 1 !== 0
    let stars = '★'.repeat(fullStars)
    if (hasHalf) stars += '☆'
    return stars
  },

  // 输入题目内容
  onQuestionInput(e) {
    this.setData({ questionText: e.detail.value })
    this.checkCanSubmit()
  },

  // 输入答案
  onAnswerInput(e) {
    this.setData({ correctAnswer: e.detail.value })
    this.checkCanSubmit()
  },

  // 输入备注
  onNoteInput(e) {
    this.setData({ noteContent: e.detail.value })
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
          const data = res.data.data
          this.setData({
            knowledgePoints: data.knowledge_points || [],
            vocabulary: data.vocabulary || []
          })
        }
      }
    })
  },

  // 检查是否可以提交
  checkCanSubmit() {
    const { questionText, correctAnswer, subjectId, gradeId, mistakeType } = this.data
    const canSubmit = questionText && correctAnswer && subjectId && gradeId && mistakeType
    this.setData({ canSubmit })
  },

  // 提交错题
  submitMistake() {
    if (!this.data.canSubmit) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' })
      return
    }
    
    const { questionText, correctAnswer, subjectId, gradeId, mistakeType, 
            difficultyLevels, difficultyIndex, noteContent, imagePath } = this.data
    
    wx.showLoading({ title: '提交中...' })
    
    const data = {
      user_id: app.globalData.userId || 'test_user',
      subject_id: subjectId,
      grade_id: gradeId,
      question_text: questionText,
      correct_answer: correctAnswer,
      mistake_type: mistakeType,
      difficulty: difficultyLevels[difficultyIndex]
    }
    
    if (noteContent) {
      data.notes = [{ type: 'text', content: noteContent }]
    }
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes',
      method: 'POST',
      data: data,
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          wx.showToast({ title: '添加成功', icon: 'success' })
          
          setTimeout(() => {
            wx.navigateBack()
          }, 1500)
        } else {
          wx.showToast({ title: res.data.error || '添加失败', icon: 'none' })
        }
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  }
})