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
	data = document.getElementById('data'+id).innerHTML
	datad = document.getElementById('datad'+id).innerHTML
	escala.value = data
	destino.value = datad
}