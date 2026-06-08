// pages/chat/chat.js
const app = getApp();

Page({
  data: {
    messages: [],
    inputText: '',
    isTyping: false,
    subjects: ['全部', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'],
    subjectIndex: 0,
    quickQuestions: [
      '这道题怎么做？',
      '帮我解释这个概念',
      '这个公式怎么用？',
      '帮我检查作业'
    ],
    scrollToView: ''
  },

  onLoad(options) {
    if (options.subject) {
      const index = this.data.subjects.indexOf(options.subject);
      if (index > -1) {
        this.setData({ subjectIndex: index });
      }
    }
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  onSubjectChange(e) {
    this.setData({ subjectIndex: e.detail.value });
  },

  sendMessage() {
    const { inputText, messages } = this.data;
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputText.trim()
    };

    this.setData({
      messages: [...messages, userMessage],
      inputText: '',
      isTyping: true
    });

    this.scrollToBottom();

    // 模拟AI回复（实际需要调用后端API）
    setTimeout(() => {
      this.receiveAIResponse(userMessage.content);
    }, 1000);
  },

  receiveAIResponse(question) {
    // 模拟AI回复 - 实际项目中需要调用后端API
    const responses = [
      '这是一个很好的问题！让我来帮你分析一下...',
      '根据你的问题，我找到了相关的知识点...',
      '这个概念其实不难理解，我们来一步步看...'
    ];

    const aiMessage = {
      id: Date.now(),
      role: 'assistant',
      content: responses[Math.floor(Math.random() * responses.length)],
      actions: true
    };

    this.setData({
      messages: [...this.data.messages, aiMessage],
      isTyping: false
    });

    this.scrollToBottom();
  },

  askQuickQuestion(e) {
    const question = e.currentTarget.dataset.question;
    this.setData({ inputText: question });
    this.sendMessage();
  },

  copyText(e) {
    const text = e.currentTarget.dataset.text;
    wx.setClipboardData({
      data: text,
      success: () => {
        wx.showToast({ title: '已复制', icon: 'success' });
      }
    });
  },

  regenerate(e) {
    const index = e.currentTarget.dataset.index;
    // 找到对应的用户问题重新提问
    const messages = this.data.messages;
    let userQuestion = '';
    for (let i = index; i >= 0; i--) {
      if (messages[i].role === 'user') {
        userQuestion = messages[i].content;
        break;
      }
    }
    if (userQuestion) {
      this.setData({ inputText: userQuestion });
      this.sendMessage();
    }
  },

  scrollToBottom() {
    const length = this.data.messages.length;
    this.setData({
      scrollToView: `msg-${length - 1}`
    });
  }
});