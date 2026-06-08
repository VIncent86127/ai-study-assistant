// pages/homework/homework.js
Page({
  data: {
    imagePath: '',
    subjects: ['数学', '语文', '英语', '物理', '化学', '生物'],
    currentSubject: '数学',
    analysisResult: null,
    homeworkHistory: [
      { id: 1, subject: '数学', title: '代数方程练习', time: '今天 14:30' },
      { id: 2, subject: '英语', title: '阅读理解', time: '昨天 20:15' }
    ]
  },

  chooseImage() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera', 'album'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        this.setData({ imagePath: tempFilePath });
        this.analyzeImage(tempFilePath);
      }
    });
  },

  analyzeImage(imagePath) {
    wx.showLoading({ title: '分析中...' });
    
    // 模拟分析结果 - 实际需要调用后端API
    setTimeout(() => {
      this.setData({
        analysisResult: {
          questionType: '计算题',
          difficulty: '中等',
          knowledgePoints: '一元二次方程、因式分解',
          solution: '1. 观察方程结构\n2. 尝试因式分解\n3. 求解方程',
          answer: 'x₁=2, x₂=3'
        }
      });
      wx.hideLoading();
    }, 2000);
  },

  selectSubject(e) {
    this.setData({ currentSubject: e.currentTarget.dataset.subject });
  },

  viewHistory(e) {
    const id = e.currentTarget.dataset.id;
    wx.showToast({ title: '加载中...', icon: 'loading' });
  }
});