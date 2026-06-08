// pages/subject/subject.js
Page({
  data: {
    subject: '数学',
    knowledgeList: [
      { id: 1, name: '一元二次方程', desc: '解方程、应用题', mastered: true, questionCount: 25 },
      { id: 2, name: '几何证明', desc: '三角形、四边形', mastered: true, questionCount: 30 },
      { id: 3, name: '函数与图像', desc: '一次函数、二次函数', mastered: false, questionCount: 28 },
      { id: 4, name: '概率统计', desc: '数据统计、概率计算', mastered: false, questionCount: 20 }
    ],
    totalPoints: 4,
    masteredPoints: 2,
    totalQuestions: 103
  },

  onLoad(options) {
    if (options.subject) {
      this.setData({ subject: options.subject });
      this.loadKnowledgeList(options.subject);
    }
  },

  loadKnowledgeList(subject) {
    // 根据学科加载知识点列表
  },

  selectKnowledge(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/chat/chat?knowledgeId=${id}`
    });
  }
});