from django.shortcuts import render
from .models import Alumnos, Comentarios
from .forms import ComentarioContactoForm
from .models import ComentariosContacto
from django.shortcuts import get_object_or_404
import datetime
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages
#accedemos al modelo alumnos que contiene la tabla

# Create your views here.

#indicamos el lugar donde se renderizara el resultado de la vista

def registros(request):
    alumnos=Alumnos.objects.all()
    return render(request,"registros/principal.html",{'alumnos':alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():#si los datos son correctos
            form.save()#inserta
            comentarios=ComentariosContacto.objects.all()
            return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})
    form = ComentarioContactoForm()
    #si algo sale mal se reenvia al formulariolos datos ingresados
    return render(request,"registros/contacto.html",{'form':form})   
     
def contacto(request):
    return render(request,"registros/contacto.html")
    #indicamos el lugar donde se reendirizara el resultado de esta vista
    #y enviamos la lista de alumsno recuperados.

def consultarComentarioContacto(request):
    comentarios=ComentariosContacto.objects.all()
    #all recupera todos los objetos del modelo

    return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})
    #indicamos el lugar donde se renderizara el resultado  enviamos la lista
    #de comentarios recuperados

def eliminarComentarioContacto(request, id, confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentariosContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentariosContacto.objects.all()
        return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})

    return render(request, confirmacion, {'object':comentario})
    
def consultarComentarioIndividual(request, id):
    comentario=ComentariosContacto.objects.get(id=id)
    #get recupera un unico resultado por busqueda de id, pide recuperar el comentario contacto dondes
    #la clave sea igual al del id

    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})
    #indicamos el lugar donde se renderizara el resultado  enviamos la lista
    #de comentarios recuperados

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentariosContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #referenciamos que el elmento del formulario pertenece al comentario ya existente
    if form.is_valid():
        form.save()
        comentarios=ComentariosContacto.objects.all()
        return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})

    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})

#funcion filter, retorna los datos que coinciden con los parametros

def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id,matricula,nombre,carrera,turno,imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')

    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar1(request):
    #filter regresa multiples archivos
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    #filter regresa multiples archivos
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    #only solo regresa lo que pides, en este caso todos los objetos por el all
    alumnos=Alumnos.objects.all().only("matricula","nombre","carrera","turno","imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    #only solo regresa lo que pides
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    #only solo regresa lo que pides
    alumnos=Alumnos.objects.filter(nombre__in=["Juan","Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio = datetime.date(2021, 7, 1)
    fechaFin = datetime.date(2021, 7, 16)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    #consultando entre modelos
    alumnos=Alumnos.objects.filter(comentarios__coment='Esto es un comentario')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
                messages.error(request, "Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})

def seguridad(request):
    return render(request,"registros/seguridad.html")