// pages/login/login.js
const app = getApp();

Page({
  data: {
    nickname: '',
    grades: ['小学一年级', '小学二年级', '小学三年级', '小学四年级', '小学五年级', '小学六年级', '初中一年级', '初中二年级', '初中三年级', '高中一年级', '高中二年级', '高中三年级'],
    gradeIndex: -1
  },

  onNicknameInput(e) {
    this.setData({ nickname: e.detail.value });
  },

  onGradeChange(e) {
    this.setData({ gradeIndex: e.detail.value });
  },

  onGetUserInfo(e) {
    if (e.detail.userInfo) {
      const userInfo = {
        nickname: e.detail.userInfo.nickName,
        avatar: e.detail.userInfo.avatarUrl,
        grade: this.data.grades[this.data.gradeIndex] || ''
      };
      this.doLogin(userInfo);
    }
  },

  onLogin() {
    const { nickname, grades, gradeIndex } = this.data;
    
    if (!nickname) {
      wx.showToast({ title: '请输入昵称', icon: 'none' });
      return;
    }

    const userInfo = {
      nickname: nickname,
      grade: gradeIndex >= 0 ? grades[gradeIndex] : ''
    };
    
    this.doLogin(userInfo);
  },

  doLogin(userInfo) {
    // 保存用户信息
    app.updateUserInfo(userInfo);
    
    wx.showToast({ title: '登录成功', icon: 'success' });
    
    setTimeout(() => {
      wx.navigateBack();
    }, 1500);
  }
});