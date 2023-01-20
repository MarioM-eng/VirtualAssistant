$(document).ready(function(){

   $('#preg-frecuentes').toggle();//Ocultamos el boton desde el cargue de la página'
   var elemento = document.getElementById('icon-preg-frecuentes');//Div que contiene el icono de ver y ocultar

   $("#btn-preg-frecuentes").click(function(evento){

      $('#preg-frecuentes').toggle();//Oculta o muestra un elemento

      if($('#preg-frecuentes').attr('style') == "display: none;"){//Si el elemento está oculto o no
	    	$(".icon-eye-off").remove();//Quitamos el elemento que contenga esta clase
	    	elemento.insertAdjacentHTML('afterbegin', '<span class="icon-eye"></span>');//Insertamos en el botónun span
      }else{
	    	$(".icon-eye").remove();
	    	elemento.insertAdjacentHTML('afterbegin', '<span class="icon-eye-off"></span>');
      }
      
   });
});