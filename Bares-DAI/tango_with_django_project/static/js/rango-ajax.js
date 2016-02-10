$('#likes').click(function(){
    var barid;
    barid = $(this).attr("data-catid");
    $.get('/rango/like_bares/', {bares_id: barid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });
    $(document).ready(function(){  
	$('#botones .boton').click(function(){ /*al hacer click en un botón*/  
		$('body').removeClass();    /*borre todas las clases*/  
			if(this.id == 'aumentar'){   /*si la clase botón tiene el ID aumentar*/  
	    		$('body').addClass('grande');  /*cargue desde el CSS la clase grande*/  
	    	}  
		else if(this.id == 'disminuir'){ /*si el ID es disminuir*/  
	    		$('body').addClass('chica'); /*cargue la clase chica*/  
		}  
		$('#botones .boton').removeClass('seleccion'); /*elimine la negrita del boton*/  
   		$(this).addClass('seleccion');/*agregue la negrita al botón activo*/  
	});                             
     });  

});
