function add_escala(){
	escala = document.getElementById('escala')
	costo = document.getElementById('costo')
	result = escala.value + " " + "$" + costo.value
	escalas = document.getElementById('escalas')
	if(escalas.value.length == 0 ){
			escalas.value = result
	}
	else
	{
		escalas.value = escalas.value + "," + result
	}
	escala.value = ""
	costo.value = ""
}

function seleccion(id){
	id = id
	destino = document.getElementById('destino')
	escala = document.getElementById('escala') 
	
	datad = document.getElementById('datad'+id).innerHTML
	data = document.getElementById('data'+id).innerHTML
	escala.value = data
	destino.value = datad
}

function add_hora(){
	horas = document.getElementById('hora')
	minutos = document.getElementById('minuto')
	result = horas.value+':'+minutos.value
	if(horarios.value.length == 0){
		horarios.value = result
	}
	else
	{
		horarios.value = horarios.value + ',' + result
	}
	
}

function reset(){
	escala = document.getElementById('escala')
	horarios = document.getElementById('horarios')
	escala.value = ""
	horarios.value = ""
}