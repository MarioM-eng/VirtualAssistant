$(document).ready(function(){
   $("#cabecera-min").click(function(evento){
      $('#contenido-msg-chat').toggle();//Oculta o muestra un elemento
      if($('#contenido-msg-chat').attr('style') == "display: none;"){//Si el elemento está oculto o no
      		var elemento = document.getElementById('minimizar-chat');
	    	$(".icon-minimize-2").remove();//Quitamos el elemento que contenga esta clase
	    	elemento.insertAdjacentHTML('afterbegin', '<span class="icon-maximize-2"></span>');//Insertamos en el botónun span
      }else{
      		var elemento = document.getElementById('minimizar-chat');
	    	$(".icon-maximize-2").remove();
	    	elemento.insertAdjacentHTML('afterbegin', '<span class="icon-minimize-2"></span>');
      }
   });
});