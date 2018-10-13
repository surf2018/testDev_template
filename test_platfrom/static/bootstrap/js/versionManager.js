var verList=$('#vertable').children('tr')
for (var i=0;i<verList.length;i++){
  var tr=verList.eq(i)
  var tdobject=verList.eq(i).find('td')
  var release=tdobject.eq(3).text()
    if(release=='Y') {
        tr.css("background", "yellow")
    }
}
