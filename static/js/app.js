function activeMenuOption(href) {
    $(".app-menu .nav-link")
    .removeClass("active")
    .removeAttr('aria-current')

    $(`[href="${(href ? href : "#/")}"]`)
    .addClass("active")
    .attr("aria-current", "page")
}

const app = angular.module("angularjsApp", ["ngRoute"])
app.config(function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix("")

    $routeProvider
    .when("/", {
        templateUrl: "/dashboard",
        controller: "dashboardCtrl"
    })
    .when("/login", {
        templateUrl: "/login",
        controller: "appCtrl"
    })
    .when("/categorias", {
        templateUrl: "/categorias",
        controller: "categoriasCtrl"
    })
    .when("/pendientes", {
        templateUrl: "/pendientes",
        controller: "pendientesCtrl"
    })
    .when("/recordatorios", {
        templateUrl: "/recordatorios",
        controller: "recordatoriosCtrl"
    })
    .otherwise({
        redirectTo: "/"
    })
})

app.run(["$rootScope", "$location", "$timeout", function($rootScope, $location, $timeout) {
    function actualizarFechaHora() {
        lxFechaHora = DateTime
        .now()
        .setLocale("es")

        $rootScope.angularjsHora = lxFechaHora.toFormat("hh:mm:ss a")
        $timeout(actualizarFechaHora, 1000)
    }

    $rootScope.slide = ""

    actualizarFechaHora()

    $rootScope.$on("$routeChangeSuccess", function (event, current, previous) {
        $("html").css("overflow-x", "hidden")
        
        const path = current.$$route.originalPath

        if (path.indexOf("splash") == -1) {
            const active = $(".app-menu .nav-link.active").parent().index()
            const click  = $(`[href^="#${path}"]`).parent().index()

            if (active != click) {
                $rootScope.slide  = "animate__animated animate__faster animate__slideIn"
                $rootScope.slide += ((active > click) ? "Left" : "Right")
            }

            $timeout(function () {
                $("html").css("overflow-x", "auto")

                $rootScope.slide = ""
            }, 1000)

            activeMenuOption(`#${path}`)
        }
    })
}])

app.controller("appCtrl", function ($scope, $http) {
    console.log("appCtrl loaded")
    
    $(document).ready(function() {        
        $("#frmInicioSesion").off("submit").on("submit", function (event) {
            event.preventDefault()
            
            const formData = $(this).serialize()
            
            $.post("iniciarSesion", formData, function (respuesta) {
                if (respuesta.success) {
                    alert("Iniciaste Sesión")
                    window.location.href = "/"
                    return
                }
                alert("Usuario y/o Contraseña Incorrecto(s)")
            }).fail(function(xhr, status, error) {
                console.log("Login failed:", error, xhr.responseText)
                alert("Error en el login: " + error)
            })
        })
    })
})

app.controller("dashboardCtrl", function ($scope, $http) {
    // Load statistics when dashboard loads
    $scope.$on('$viewContentLoaded', function() {
        // Small delay to ensure DOM is ready
        setTimeout(function() {
            if (typeof cargarEstadisticas === 'function') {
                cargarEstadisticas();
            }
        }, 100);
    });
})

app.controller("categoriasCtrl", function ($scope, $http) {
    function buscarCategorias() {
        $.get("/tbodyCategorias", function (trsHTML) {
            $("#tbodyCategorias").html(trsHTML)
        })
    }

    buscarCategorias()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true

    var pusher = new Pusher("2922c4803975e3f70a0d", {
        cluster: "us2"
    })

    var channel = pusher.subscribe("canalCategorias")
    channel.bind("eventoCategorias", function(data) {
        buscarCategorias()
    })

    $(document).off("submit", "#frmCategoria")
    $(document).on("submit", "#frmCategoria", function (event) {
        event.preventDefault()

        $.post("/categoria", {
            id: $("#frmCategoria").data("edit-id") || "",
            nombre: $("#txtNombre").val()
        }, function() {
            $("#frmCategoria")[0].reset()
            $("#frmCategoria").removeData("edit-id")
            buscarCategorias()
        })
    })

    // Edit categoria
    $(document).on("click", ".btn-editar-categoria", function (event) {
        const id = $(this).data("id")
        const nombre = $(this).data("nombre")
        
        $("#txtNombre").val(nombre)
        $("#frmCategoria").data("edit-id", id)
        $("#txtNombre").focus()
    })

    // Delete categoria
    $(document).on("click", ".btn-eliminar-categoria", function (event) {
        const id = $(this).data("id")
        
        if (confirm("¿Estás seguro de que quieres eliminar esta categoría?")) {
            $.ajax({
                url: `/categoria/${id}`,
                type: "DELETE",
                success: function() {
                    buscarCategorias()
                    toast("Categoría eliminada correctamente", 2)
                },
                error: function() {
                    toast("Error al eliminar la categoría", 2)
                }
            })
        }
    })
})

app.controller("pendientesCtrl", function ($scope, $http) {
    function buscarPendientes() {
        $.get("/tbodyPendientes", function (trsHTML) {
            $("#tbodyPendientes").html(trsHTML)
        })
    }

    buscarPendientes()

    function cargarCategorias() {
        $.get("/categorias/all", function (data) {
            const select = $("#selectCategoria")
            select.empty()
            select.append('<option value="">Seleccionar categoría</option>')
            
            data.forEach(function(categoria) {
                select.append(`<option value="${categoria.idCategoria}">${categoria.nombreCategoria}</option>`)
            })
        })
    }

    cargarCategorias()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true

    var pusher = new Pusher("52712e9b9d8935dc32c5", {
      cluster: "us2"
    })

    var channel = pusher.subscribe("canalPendientes")
    channel.bind("eventoPendientes", function(data) {
        buscarPendientes()
    })

    $(document).off("submit", "#frmPendiente")
    $(document).on("submit", "#frmPendiente", function (event) {
        event.preventDefault()

        $.post("/pendiente", {
            id: $("#frmPendiente").data("edit-id") || "",
            titulo: $("#txtTitulo").val(),
            descripcion: $("#txtDescripcion").val(),
            estado: $("#txtEstado").val(),
            idCategoria: $("#selectCategoria").val()
        }, function() {
            $("#frmPendiente")[0].reset()
            $("#frmPendiente").removeData("edit-id")
            buscarPendientes()
        })
    })

    // Edit pendiente
    $(document).on("click", ".btn-editar-pendiente", function (event) {
        const id = $(this).data("id")
        const titulo = $(this).data("titulo")
        const descripcion = $(this).data("descripcion")
        const estado = $(this).data("estado")
        const categoria = $(this).data("categoria")
        
        $("#txtTitulo").val(titulo)
        $("#txtDescripcion").val(descripcion)
        $("#txtEstado").val(estado)
        $("#selectCategoria").val(categoria)
        $("#frmPendiente").data("edit-id", id)
        $("#txtTitulo").focus()
    })

    // Delete pendiente
    $(document).on("click", ".btn-eliminar-pendiente", function (event) {
        const id = $(this).data("id")
        
        if (confirm("¿Estás seguro de que quieres eliminar este pendiente?")) {
            $.ajax({
                url: `/pendiente/${id}`,
                type: "DELETE",
                success: function() {
                    buscarPendientes()
                    toast("Pendiente eliminado correctamente", 2)
                },
                error: function() {
                    toast("Error al eliminar el pendiente", 2)
                }
            })
        }
    })
})

app.controller("recordatoriosCtrl", function ($scope, $http) {
    function buscarRecordatorios() {
        $.get("/tbodyRecordatorios", function (trsHTML) {
            $("#tbodyRecordatorios").html(trsHTML)
        })
    }

    function cargarPendientes() {
        $.get("/pendientes/all", function (data) {
            const select = $("#selectPendiente")
            select.empty()
            select.append('<option value="">Seleccionar pendiente</option>')
            
            data.forEach(function(pendiente) {
                select.append(`<option value="${pendiente.idPendiente}">${pendiente.tituloPendiente}</option>`)
            })
        })
    }

    function cargarCategorias() {
        $.get("/categorias/all", function (data) {
            const select = $("#selectCategoriaRecordatorio")
            select.empty()
            select.append('<option value="">Seleccionar categoría</option>')
            
            data.forEach(function(categoria) {
                select.append(`<option value="${categoria.idCategoria}">${categoria.nombreCategoria}</option>`)
            })
        })
    }

    buscarRecordatorios()
    cargarPendientes()
    cargarCategorias()
    

    $(document).off("submit", "#frmRecordatorio")
    $(document).on("submit", "#frmRecordatorio", function (event) {
        event.preventDefault()

        const editId = $("#frmRecordatorio").data("edit-id")
        const data = {
            idPendiente: $("#selectPendiente").val(),
            idCategoria: $("#selectCategoriaRecordatorio").val(),
            mensaje: $("#txtMensaje").val(),
            fechaHora: $("#txtFechaHora").val()
        }

        if (editId) {
            // Update existing recordatorio
            $.ajax({
                url: `/recordatorio/${editId}`,
                type: "PUT",
                data: data,
                success: function() {
                    $("#frmRecordatorio")[0].reset()
                    $("#frmRecordatorio").removeData("edit-id")
                    buscarRecordatorios()
                }
            })
        } else {
            // Create new recordatorio
            $.post("/recordatorio", data, function() {
                $("#frmRecordatorio")[0].reset()
                buscarRecordatorios()
            })
        }
    })

    // Edit recordatorio
    $(document).on("click", ".btn-editar-recordatorio", function (event) {
        const id = $(this).data("id")
        
        $.get(`/recordatorio/${id}`, function (data) {
            if (data.idRecordatorio) {
                $("#selectPendiente").val(data.idPendiente)
                $("#selectCategoriaRecordatorio").val(data.idCategoria)
                $("#txtMensaje").val(data.mensaje)
                // Format datetime for input
                const fechaHora = new Date(data.fechaHora)
                const formatted = fechaHora.toISOString().slice(0, 16)
                $("#txtFechaHora").val(formatted)
                $("#frmRecordatorio").data("edit-id", id)
            }
        })
    })

    // Delete recordatorio
    $(document).on("click", ".btn-eliminar-recordatorio", function (event) {
        const id = $(this).data("id")
        
        if (confirm("¿Estás seguro de que quieres eliminar este recordatorio?")) {
            $.ajax({
                url: `/recordatorio/${id}`,
                type: "DELETE",
                success: function() {
                    buscarRecordatorios()
                    toast("Recordatorio eliminado correctamente", 2)
                },
                error: function() {
                    toast("Error al eliminar el recordatorio", 2)
                }
            })
        }
    })
})

const DateTime = luxon.DateTime
let lxFechaHora

document.addEventListener("DOMContentLoaded", function (event) {
    const configFechaHora = {
        locale: "es",
        weekNumbers: true,
        // enableTime: true,
        minuteIncrement: 15,
        altInput: true,
        altFormat: "d/F/Y",
        dateFormat: "Y-m-d",
        // time_24hr: false
    }

    activeMenuOption(location.hash)
})

