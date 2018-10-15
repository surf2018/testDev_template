var verList=$('#vertable').children('tr')
for (var i=0;i<verList.length;i++){
  var tr=verList.eq(i)
  var tdobject=tr.find('td')
  var release=tdobject.eq(5).text()
    if(release=='True') {
      console.log(release)
        tr.css("background", "yellow")
    }
}
