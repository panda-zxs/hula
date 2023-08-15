#! /bin/bash
git remote remove origin
git remote add origin https://panda-zxs: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@github.com/panda-zxs/hula.git
git config user.email "45396622zxs@gmail.com"
git config user.name "panda-zxs"
git config pull.rebase false
git checkout -- .
git fetch origin
git pull origin master
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

<<<<<<< HEAD
git push origin master << eof

panda-zxs

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

eof
done
=======
git push origin master
done
>>>>>>> ce420068fad878837cef6a79b16d2a0cb0caacae
