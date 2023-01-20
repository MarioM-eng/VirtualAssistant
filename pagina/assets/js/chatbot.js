var me = {};
me.avatar = "usuario.png";

var bot = {};
bot.avatar = "bot2.JFIF";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

function insertChat(who, text){
	
	
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){
        control = '<div class="text-break bg-primary shadow-lg d-inline-block mensaje-user">' +
                    '<p class="text-white" style="margin: 0;">' + text + '</p>'+
                    '<small class="text-light">'+date+'</small>'+
                  '</div><hr>';
        insert(control)                  
    }else if(who == "bot" &&  text[1] == undefined){

      control = '<div class="text-break bg-white shadow-lg bounce animated mensaje-bot">' +
                  '<p class="text-secondary" style="margin: 0;">' + text[0].text + '</p>'+
                  '<small class="text-muted">'+date+'</small>'+
                '</div><hr>';
      insert(control);

    }else{

      control = '<div class="text-break bg-white shadow-lg bounce animated mensaje-bot">' +
                  '<p class="text-secondary" style="margin: 0;">' + text[0].text + '</p>'+
                  '<small class="text-muted">'+date+'</small>'+
                '</div><hr>';
      insert(control);

      link = "";//Variable para almacenar todos los elementos de "Te puede interesar" en etiquetas <a>
      text.forEach(function(texto,index){
        if (index != 0) {//Si no es el primer elemento
          if (index == 1) {//si es el segundo elemento
            link = link + texto.text + "<br>";
          }else if ((text.length - 1) != index) { //si no es el último
            link = link + "<a class=\"inter\" href=\"#\">"+texto.text+"</a><br>";
          }else{//Si es el último elemento
            link = link + texto.text;
          }
        }
      }); 
      setTimeout(function(){
        writing = "<div id=\"escribiendo\" style=\"margin: 20px;\"><p class=\"flash animated\">Escribiendo...</p><hr></div>"
      $("#mensajes-chat").append(writing).scrollTop($("#mensajes-chat").prop('scrollHeight'));
      },500);
    
      setTimeout(function(){
        $('#escribiendo').fadeOut();
        $('#escribiendo').remove(); 
        if(link != ""){//Si hay interes
          control = '<div class="text-break bg-white shadow-lg mensaje-bot">' +
                      '<p class="text-secondary" style="margin: 0;">'+ link +'</p>'+
                      '<small class="text-muted">'+date+'</small>'+
                    '</div><hr>';
          insert(control);
          interesar();
        }
      },2000);
    }
}

//-- No use time. It is a javaScript effect.
function insert(control, time){
  if (time === undefined){
        time = 0;
    }
  setTimeout(
        function(){                        
            $("#mensajes-chat").append(control).scrollTop($("#mensajes-chat").prop('scrollHeight'));
        }, time);
}

$(document).ready(function(){interesar();});

function interesar(){//Función para al darle click a los link, se envie el texto a rasa
  setTimeout(function(){
    $('.inter').click(function(event) {
      event.preventDefault();
      console.log($(this).text());
      submitMessage($(this).text());
    });
  },3);
}

function resetChat(){
    $("#mensajes-chat").empty();
}

$(".mytext").on("keydown", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            insertChat("me", text);              
            $(this).val('');
        }
    }
});

$('body > div > div > div:nth-child(2) > span').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
})


function submitMessage(text)
   {
    insertChat("me", text);
    sendMessage(text);
    $('#mytext').val('');
   }

function sendMessage(texto)
{
     var xhttp = new XMLHttpRequest();

     xhttp.onreadystatechange = function() {//Este método se ejecuta cuando enviamos un mensaje al servidor
       if (this.readyState == 4 && this.status == 200) {
        var dataJson = eval(this.responseText);//Se recibe la respuesta del servidor en la variable dataJson
        if (dataJson != undefined) {//si dataJson está definida(recibió el mensaje)
          pararCronometro();//Se para el cronómetro
          ml = 0;//Se restablecen los valores de milisegundo y segundo a 0
          s = 0;
        }
        writing = "<div id=\"escribiendo\" style=\"margin: 20px;\"><p class=\"flash animated\">Escribiendo...</p><hr></div>"
        $("#mensajes-chat").append(writing).scrollTop($("#mensajes-chat").prop('scrollHeight'));
        setTimeout(function(){ 
          $('#escribiendo').fadeOut();
          $('#escribiendo').remove();
          insertChat("bot", dataJson); 
        },1000);
       }
     };
	 	 
     xhttp.open("POST", "http://localhost:5005/webhooks/rest/webhook");
     xhttp.setRequestHeader("Content-Type", "application/json");
     if (true) {
      iniciarCronometro();
      id = setInterval(iniciarCronometro,10);//El método se ejecutará cada 10 milisegundos o 0.01 segundos
      xhttp.send(JSON.stringify({message:texto}));//Aquí se manda el mensaje al servidor  
     }
	 
}

//Crearemos un cronometro para averiguar cuanto tarda el bot en dar una respuesta
// - Definimos las variables globales para que se puedan acceder desde cualquier parte del código
ml = 0;//Variable que contendrá los milisegundos
s = 0//Variable que contendrá los segundos
function iniciarCronometro(){
    var sAux, mlAux;//valores auxiliares para contener los segundos milisegundos
    ml++;//Aumentamos en 1 el milisegundo
    if (ml>99){s++;ml=0;}//si se alcanzan los 99 milisegundos la variable ml se iguala a 0 y la variable segundo se aumenta en 1
    if (s>59){s=0;}//si se alcanzan los 59 segundos la variable s se iguala a 0

    if (s<10){mlAux=0+ml;}else{mlAux=ml;}
    if (s<10){sAux=0+s;}else{sAux=s;}

    console.log(sAux + ":" + mlAux); 
}

function pararCronometro(){
    clearInterval(id);
}
  

$(document).ready(function() 
   {

   $(".mytext").on("keyup", function(e)
      {
      if ((e.keyCode || e.which) == 13)
         {
         var text = $(this).val();
         if (text !== "")
            {
              submitMessage(text);   
              $(this).val('');
            }
         }
      });

   $("#enviar").on("click", function(e)
      {
        e.preventDefault();
      var text = $('#mytext').val();
      if (text !== "")
         {
         submitMessage(text); 
         $(this).val('');
         }
      });
   
   

        
      
   });


//-- NOTE: No use time on insertChat.
