var main =  document.getElementById("main");
var bubble = document.getElementById("bubble")
function change(){
    main.style = "background-image: url('/static/images/404-bubbles-blue.png')";
    bubble.style = "background-image: url('/static/images/404-blue.png')";
    bubble.lastElementChild.innerHTML = "Vraťme<br>se<br>zpět";
}
function changeBack(){
    main.style = "background-image: url('/static/images/404-bubbles-red.png')";
    bubble.style = "background-image: url('/static/images/404-red.png')";
    bubble.lastElementChild.innerHTML = " Error<br>404";
}