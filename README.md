# LOL Team Challenge Helper
> 英雄聯盟挑戰系統陣容小幫手

## 使用說明

### 名詞解釋

- 必選條件：五人皆需使用條件中的英雄
- 可選條件：五人中至少三人需使用條件中的英雄，不需全部使用，顯示時會排除不在必選條件內的英雄
- 完全符合：符合所有必選條件和可選條件

### 顯示區塊

顯示之英雄皆會滿足「必選條件」，即已排除不在必選條件內的英雄

1. **符合「所有條件」的英雄**
    此區塊內的英雄符合所有選擇條件，可直接使用
2. **符合「必選條件」，但不符合所有條件的英雄**：
    此區塊內的英雄皆符合必選條件，唯仍需注意有沒有滿足所有可選條件
3. **{可選條件} 需要從以下英雄中選擇至少3個英雄**：
    此區塊內的英雄已排除不在必選條件內的英雄，唯仍需注意有沒有滿足所有可選條件
4. **以下英雄符合「可選條件」中的{N}個條件，推薦使用**
    顯示符合最多可選條件的英雄，此區塊內的英雄已排除不在必選條件內的英雄

## 部署

### Heroku CLI 安裝

- https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

### Connect to Heroku

1. 註冊: https://signup.heroku.com

2. 創建Heroku project

3. CLI Login

  `heroku login` or `heroku auth:login`

### 上傳到

1. 將heroku添加為git remote

  `heroku git:remote -a {HEROKU_APP}`

2. 檢查是否有在remote list中

  `git remote -v`

3. commit並push到remote，會在終端顯示部署進度

  ```
  git add .
  git commit -m "Add code"
  git push heroku master
  ```
