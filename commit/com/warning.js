function huisu(s, index, total, data, len) {
  if (index >= total) {
      console.log('huisu', s)
      return
  }
  len = s.length
  for (let i = 0; i < total; i++) {
      if (s.indexOf(data[i]) !== -1) continue
      s += data[i]
      huisu(s, index + 1, total, data, 0)
      s = s.substr(0, len)
  }
}

let data = ['foo', 'bar', 'then']
huisu('', 0, data.length, data, 0)


function getName({ nickname, age, height }) {
  console.log(nickname, age, height)
}

getName({ height: 100 })


function huisu(value, index, len, arr, current) {
  if (index >= len) {
      if (value === 8) {
          console.log('suu', current)
      }
      console.log('suu', current)
      return
  }
  for (let i = index; i < len; i++) {
      current.push(arr[i])
      console.log('suu', current)
      if (value + arr[i] === 8) {
          console.log('结果', current)
          return
      }
      huisu(value + arr[i], i + 1, len, arr, [...current])
      console.log('suu', value)
      current.pop()
      onsole.log('suu', current)
  }
}

const arrData = [1, 3, 5, 4, 7, 8]
onsole.log('suu', arrData)
huisu(0, 0, arrData.length, arrData, [])

let toDate = new Date();
onsole.log('suu', toDate)
new Date(toDate.getFullYear(), toDate.getMonth() - i)
onsole.log('suu', new Date(toDate.getFullYear(), toDate.getMonth() - i))