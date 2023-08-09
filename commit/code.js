const path = require('path');
const fs = require('fs');

const MIN_COUNT = 6;

// 写入文件
function writeFile(distFilePath, content) {
  try {
    fs.writeFileSync(distFilePath, content);
  } catch (e) {
    console.error('writeFile', e);
  }
}

// 读取文件
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    console.error('readFile', e);
  }
}

// 实现准备好的文件名称，随机也可以
const JS_NAMES = ['index.js', 'main.js', 'code.js', 'app.js', 'visitor.js', 'detail.js', 'warning.js', 'product.js', 'comment.js', 'awenk.js', 'test.js'];
// 创建新的代码文件
function createFile(codeDir) {
  const ran = Math.floor(Math.random() * JS_NAMES.length);
  const name = JS_NAMES[ran];
  const filePath = `${codeDir}/${name}`;
  const content = getCode();
  writeFile(filePath, content);
}

// 实现准备好的样例代码
// 可以准备更多，然后随机获取
function getCode() {
  const filePath = path.resolve(__dirname, '../example/file.js');
  return readFile(filePath);
}

// 随机删除一个文件
function rmFile(codeFiles) {
  const ran = Math.floor(Math.random() * codeFiles.length);
  const filePath = codeFiles[ran];
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  } catch (e) {
    console.error('removeFile', e);
  }
}

// 代码生成目标地址
const codeDir = path.resolve(__dirname, './com');
const files = fs.readdirSync(codeDir);
// 代码文件
const codeFiles = [];
files.forEach((element) => {
  const filePath = path.resolve(`${codeDir}/${element}`);
  codeFiles.push(filePath);
});
if (codeFiles.length > MIN_COUNT) {
  rmFile(codeFiles);
} else {
  createFile(codeDir);
}
