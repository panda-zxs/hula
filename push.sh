#! /bin/bash
git checkout -- .
git config user.email "bot@example.com"
git config user.name "a bot"
git config pull.rebase false
git remote add bot https://github.com/panda-zxs/hula.git
git fetch
git pull origin master
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

git push origin master
done
