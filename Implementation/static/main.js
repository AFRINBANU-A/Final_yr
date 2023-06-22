$ = function(id) {
    return document.getElementById(id);
  }
  
  var show = function(id) {
      $(id).style.display ='block';
  }
  var hide = function(id) {
      $(id).style.display ='none';
  }

function sumbitMarks(){
    var maths = parseInt(document.getElementById('Maths').value)
    var chemistry =parseInt(document.getElementById('Chemistry').value)
    var physics = parseInt(document.getElementById('Physics').value)

    var cutoff 

    chemistry /= 2;
    physics /= 2;
    console.log(chemistry);

    cutoff = maths+chemistry+physics

    document.getElementById('result').innerHTML = cutoff
}