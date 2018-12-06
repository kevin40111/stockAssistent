# **環境建置**
[開發需求工具](https://hackmd.io/s/rJLWLWx_Q#Install-pip)

### Step1 複製程式碼
```
##終端機打開進入到你想放程式的目錄##
git clone https://github.com/kevin40111/ntust-hci-group5.git
```

### Step2 放入你自己的 .env 擋到複製下來的目錄中

### Step3 安裝依賴的套件
```
##python要先安裝pipenv##
pipenv install
```

### Step4 開啟服務
```
pipenv shell
honcho start -f Procfile.dev
line-simulator
```
- - - -

# ##撰寫方式##
### 需求
實作各檔案 reply 的方法，編寫要回傳的訊息，回傳資料型態為字串．

### 對應
目前已將關鍵字對應的檔案添加進map中
```
map = {
        '災害': 'disaster',
        '預防': 'prevention',
        '檢測': 'detection',
        '交通': 'traffic',
        '歷史資料': 'history',
    }
```

### 測試
在模擬器中輸入  歷史:  <parameter> ， 目前使用 : 符號來決定功能模組．
- - - -

# **上傳檔案**
### 建立分支
```
git checkout -b <分之名稱>
```

### 推到git hub上
```
##origin 一般是遠端pull下來預設的名稱##
git remeote -v ##查看遠儲存體位置##
git push origin
```