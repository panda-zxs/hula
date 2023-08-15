#! /bin/bash
git remote add bot https://github.com/panda-zxs/hula.git
git config user.email "45396622zxs@gmail.com"
git config user.name "zxs"
git config pull.rebase false
git checkout -- .
git fetch bot
git pull bot master
cd $(dirname $0)

# 执行次数
count=$(node ./commit/ran.js)
echo $count

# 循环执行
for((i=0;i<$count;i++))
do
node ./commit/code.js
git add .

msg=$(node ./commit/msg.js)
git commit -m "$msg"

spawn git push bot master
expect "Username"
send "panda-zxs\r"
expect "Password"
send "45396622zxs\r"
done