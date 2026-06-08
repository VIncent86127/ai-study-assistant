// app.js - AI学习助手小程序入口
App({
  globalData: {
    // 后端API地址
    apiBaseUrl: 'https://api.study-assistant.example.com',
    
    // 用户信息
    userInfo: null,
    
    // 学习进度缓存
    studyProgress: null,
    
    // 学科列表
    subjects: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'],
    
    // 年级列表
    grades: ['小学一年级', '小学二年级', '小学三年级', '小学四年级', '小学五年级', '小学六年级', '初中一年级', '初中二年级', '初中三年级', '高中一年级', '高中二年级', '高中三年级']
  },

  onLaunch() {
    // 检查登录状态
    this.checkLoginStatus();
    
    // 初始化本地缓存
    this.initLocalCache();
  },

  checkLoginStatus() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },

  initLocalCache() {
    // 初始化学习进度缓存
    const progress = wx.getStorageSync('studyProgress');
    if (progress) {
      this.globalData.studyProgress = progress;
    }
  },

  // 更新用户信息
  updateUserInfo(userInfo) {
    this.globalData.userInfo = userInfo;
    wx.setStorageSync('userInfo', userInfo);
  },

  // 更新学习进度
  updateStudyProgress(progress) {
    this.globalData.studyProgress = progress;
    wx.setStorageSync('studyProgress', progress);
  },

  // 清除用户数据（退出登录）
  clearUserData() {
    this.globalData.userInfo = null;
    this.globalData.studyProgress = null;
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('studyProgress');
  }
});