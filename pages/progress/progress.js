// pages/progress/progress.js
Page({
  data: {
    totalQuestions: 128,
    studyDays: 15,
    masteredPoints: 42,
    subjectProgress: [
      { subject: '数学', percent: 75 },
      { subject: '英语', percent: 60 },
      { subject: '物理', percent: 45 },
      { subject: '语文', percent: 80 }
    ],
    knowledgePoints: [
      { name: '一元二次方程', status: '已掌握', level: 'mastered' },
      { name: '定语从句', status: '学习中', level: 'learning' },
      { name: '牛顿定律', status: '学习中', level: 'learning' },
      { name: '几何证明', status: '已掌握', level: 'mastered' }
    ],
    suggestions: [
      '建议加强物理力学的练习，目前掌握度较低',
      '英语定语从句是难点，可以多做专项练习',
      '数学进度良好，可以尝试更高难度的题目'
    ]
  },

  onLoad() {
    this.loadProgress();
  },

  loadProgress() {
    // 从缓存或服务器加载进度数据
  }
});