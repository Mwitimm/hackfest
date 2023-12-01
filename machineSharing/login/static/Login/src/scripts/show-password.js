let showP = document.getElementById("show-password");

showP.addEventListener("click", function(){

    let input = document.querySelector('#password');

        if(input.getAttribute('type') == 'password'){
            input.setAttribute('type', 'text');
            document.getElementById("show-password").innerHTML="Ocultar";
        } else {
            input.setAttribute('type', 'password');
            document.getElementById("show-password").innerHTML="Mostrar";
        }
});