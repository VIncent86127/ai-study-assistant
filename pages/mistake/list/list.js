// pages/mistake/list/list.js
const app = getApp()

Page({
  data: {
    mistakes: [],
    totalCount: 0,
    pendingCount: 0,
    masteredCount: 0,
    loading: false,
    hasMore: true,
    page: 1,
    perPage: 20,
    
    subjectFilter: ['全部学科', '语文', '数学', '英语', '物理', '化学'],
    subjectFilterIndex: 0,
    subjectId: null,
    
    statusFilter: ['全部状态', '待复习', '已掌握'],
    statusFilterIndex: 0,
    status: null
  },

  onLoad() {
    this.loadMistakes()
    this.loadStatistics()
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true })
    this.loadMistakes(() => {
      wx.stopPullDownRefresh()
    })
    this.loadStatistics()
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMore()
    }
  },

  // 加载错题列表
  loadMistakes(callback) {
    this.setData({ loading: true })
    
    const { page, perPage, subjectId, status } = this.data
    const params = {
      user_id: app.globalData.userId || 'default',
      page,
      per_page: perPage
    }
    
    if (subjectId) params.subject_id = subjectId
    if (status) params.status = status
    
    wx.request({
      url: app.globalData.apiBase + '/api/mistakes',
      data: params,
      success: (res) => {
        if (res.data.success) {
          const mistakes = page === 1 
            ? res.data.data 
            : [...this.data.mistakes, ...res.data.data]
          
          this.setData({
            mistakes,
            hasMore: res.data.data.length >= perPage,
            page
          })
        }
      },
      complete: () => {
        this.setData({ loading: false })
        if (callback) callback()
      }
    })
  },

  // 加载统计数据
  loadStatistics() {
    wx.request({
      url: app.globalData.apiBase + '/api/statistics',
      data: { user_id: app.globalData.userId || 'default' },
      success: (res) => {
        if (res.data.success) {
          const stats = res.data.data
          let pending = 0, mastered = 0, total = 0
          
          stats.by_status.forEach(s => {
            total += s.count
            if (s.status === 'pending') pending = s.count
            if (s.status === 'mastered') mastered = s.count
          })
          
          this.setData({
            totalCount: total,
            pendingCount: pending,
            masteredCount: mastered
          })
        }
      }
    })
  },

  // 学科筛选
  onSubjectFilter(e) {
    const index = parseInt(e.detail.value)
    const subjectId = index === 0 ? null : index
    
    this.setData({
      subjectFilterIndex: index,
      subjectId,
      page: 1,
      hasMore: true,
      mistakes: []
    })
    
    this.loadMistakes()
  },

  // 状态筛选
  onStatusFilter(e) {
    const index = parseInt(e.detail.value)
    const statusMap = [null, 'pending', 'mastered']
    
    this.setData({
      statusFilterIndex: index,
      status: statusMap[index],
      page: 1,
      hasMore: true,
      mistakes: []
    })
    
    this.loadMistakes()
  },

  // 加载更多
  loadMore() {
    this.setData({ page: this.data.page + 1 })
    this.loadMistakes()
  },

  // 跳转到详情
  goToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/mistake/detail/detail?id=${id}`
    })
  },

  // 跳转到添加
  goToAdd() {
    wx.navigateTo({
      url: '/pages/mistake/add/add'
    })
  }
})