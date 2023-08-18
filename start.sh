#! /bin/bash
git remote remove bot
git remote add bot git@github.com:panda-zxs/hula.git
git config user.email "45396622zxs@gmail.com"
git config user.name "panda-zxs"
git config pull.rebase true
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
git add . --all

msg=$(node ./commit/msg.js)
git commit -m "$msg"

done
git push bot master
