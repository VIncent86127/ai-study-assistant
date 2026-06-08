// pages/mistake/detail/detail.js
const app = getApp()

Page({
  data: {
    mistakeId: null,
    mistake: {},
    knowledgePoints: [],
    vocabulary: [],
    notes: [],
    reviewHistory: [],
    
    showNoteModal: false,
    newNoteContent: ''
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
  }
})