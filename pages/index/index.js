// pages/index/index.js
Page({
  data: {
    userInfo: null,
    subjects: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'],
    subjectIcons: {
      '语文': '📖',
      '数学': '📐',
      '英语': '🔤',
      '物理': '⚡',
      '化学': '🧪',
      '生物': '🌱',
      '历史': '🏛️',
      '地理': '🌍',
      '政治': '⚖️'
    },
    recommendations: [
      { id: 1, icon: '📝', title: '数学几何难题解析', desc: '三角形面积计算技巧' },
      { id: 2, icon: '🔤', title: '英语语法专项训练', desc: '定语从句用法详解' },
      { id: 3, icon: '⚡', title: '物理力学知识点', desc: '牛顿定律应用实例' }
    ],
    todayQuestions: 0,
    totalQuestions: 0,
    weeklyQuestions: 0,
    masteredPoints: 0,
    studyDays: 0,
    accuracyRate: 0
  },

  onLoad() {
    this.loadUserInfo();
    this.loadStudyStats();
  },

  onShow() {
    this.loadUserInfo();
    this.loadStudyStats();
  },

  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo');
    this.setData({ userInfo });
  },

  loadStudyStats() {
    const progress = wx.getStorageSync('studyProgress') || {};
    this.setData({
      todayQuestions: progress.todayQuestions || 0,
      totalQuestions: progress.totalQuestions || 0,
      weeklyQuestions: progress.weeklyQuestions || 0,
      masteredPoints: progress.masteredPoints || 0,
      studyDays: progress.studyDays || 0,
      accuracyRate: progress.accuracyRate || 0
    });
  },

  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  },

  goToChat() {
    wx.switchTab({
      url: '/pages/chat/chat'
    });
  },

  goToHomework() {
    wx.switchTab({
      url: '/pages/homework/homework'
    });
  },

  goToProgress() {
    wx.switchTab({
      url: '/pages/progress/progress'
    });
  },

  goToSubject() {
    wx.navigateTo({
      url: '/pages/subject/subject'
    });
  },

  selectSubject(e) {
    const subject = e.currentTarget.dataset.subject;
    wx.navigateTo({
      url: `/pages/chat/chat?subject=${subject}`
    });
  },

  goToQuestion(e) {
    const question = e.currentTarget.dataset.question;
    wx.navigateTo({
      url: `/pages/chat/chat?title=${question.title}`
    });
  }
});