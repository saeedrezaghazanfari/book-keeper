
/* P.E.A.K.A. */

function rand(min , max){
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}

// persian digit
$(document).ready(function(){
    $('.digit').persiaNumber();
});

function showPW() {

    var x = document.getElementById("pwLOGIN");
    var y = document.getElementById('eye');
    var yy = document.getElementById('eye2');

    if (x.type === "password") {
    x.type = "text";
    y.classList.remove('fa-eye');
    y.classList.add('fa-eye-slash');
    yy.classList.remove('fa-eye');
    yy.classList.add('fa-eye-slash');

    } else {
    x.type = "password";
    y.classList.add('fa-eye');
    y.classList.remove('fa-eye-slash');
    yy.classList.add('fa-eye');
    yy.classList.remove('fa-eye-slash');
    }
}

clockDefner = () =>{
    let m;
    let a = new Date();
    let b = a.getHours();
    let c = a.getMinutes();
    let d = a.getSeconds();
    if (d < 10) { d = `0${d}` }
    if (b < 10) { b = `0${b}` }
    if (c < 10) { c = `0${c}` }
    document.getElementById('clock').innerHTML = b + " : " + c + " : " + d;
}
document.getElementById('clock').innerHTML = setInterval("clockDefner()" , 1000);  


// scroll events
// var prevScrollpos = window.pageYOffset;
// window.onscroll = function() {
//     var currentScrollPos = window.pageYOffset;
//     if (currentScrollPos < 100) {
//         document.getElementById("a").style.display = "none";
//     } else {
//         document.getElementById("a").style.display = "block";
//     }
// }
