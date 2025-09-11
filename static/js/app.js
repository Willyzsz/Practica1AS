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
        templateUrl: "/app",
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
    $("#frmInicioSesion").submit(function (event) {
        event.preventDefault()
        $.post("iniciarSesion", $(this).serialize(), function (respuesta) {
            if (respuesta.length) {
                alert("Iniciaste Sesión")
                window.location = "/#/categorias"

                return
            }

            alert("Usuario y/o Contraseña Incorrecto(s)")
        })
    })
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

    var pusher = new Pusher("e57a8ad0a9dc2e83d9a2", {
      cluster: "us2"
    })

    var channel = pusher.subscribe("canalCategorias")
    channel.bind("eventoCategorias", function(data) {
        buscarCategorias()
    })

    $(document).on("submit", "#frmCategoria", function (event) {
        event.preventDefault()

        $.post("/categoria", {
            id: "",
            nombre: $("#txtNombre").val()
        }, function() {
            $("#frmCategoria")[0].reset()
            buscarCategorias()
        })
    })

    $(document).on("click", ".btn-editar-categoria", function (event) {
        const id = $(this).data("id")
        
        $.get(`/categoria/${id}`, function (data) {
            if (data.length > 0) {
                $("#txtNombre").val(data[0].nombreCategoria)
                $("#frmCategoria").data("edit-id", id)
            }
        })
    })
})

app.controller("pendientesCtrl", function ($scope, $http) {
    function buscarPendientes() {
        $.get("/tbodyPendientes", function (trsHTML) {
            $("#tbodyPendientes").html(trsHTML)
        })
    }

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

    buscarPendientes()
    cargarCategorias()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true

    var pusher = new Pusher("e57a8ad0a9dc2e83d9a2", {
      cluster: "us2"
    })

    var channel = pusher.subscribe("canalPendientes")
    channel.bind("eventoPendientes", function(data) {
        buscarPendientes()
    })

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

    $(document).on("click", ".btn-editar-pendiente", function (event) {
        const id = $(this).data("id")
        
        $.get(`/pendiente/${id}`, function (data) {
            if (data.length > 0) {
                $("#txtTitulo").val(data[0].tituloPendiente)
                $("#txtDescripcion").val(data[0].descripcion)
                $("#txtEstado").val(data[0].estado)
                $("#selectCategoria").val(data[0].idCategoria)
                $("#frmPendiente").data("edit-id", id)
            }
        })
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
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true

    var pusher = new Pusher("e57a8ad0a9dc2e83d9a2", {
      cluster: "us2"
    })

    var channel = pusher.subscribe("canalRecordatorios")
    channel.bind("eventoRecordatorios", function(data) {
        buscarRecordatorios()
    })

    $(document).on("submit", "#frmRecordatorio", function (event) {
        event.preventDefault()

        $.post("/recordatorio", {
            id: $("#frmRecordatorio").data("edit-id") || "",
            idPendiente: $("#selectPendiente").val(),
            idCategoria: $("#selectCategoriaRecordatorio").val(),
            mensaje: $("#txtMensaje").val(),
            fechaHora: $("#txtFechaHora").val()
        }, function() {
            $("#frmRecordatorio")[0].reset()
            $("#frmRecordatorio").removeData("edit-id")
            buscarRecordatorios()
        })
    })

    $(document).on("click", ".btn-editar-recordatorio", function (event) {
        const id = $(this).data("id")
        
        $.get(`/recordatorio/${id}`, function (data) {
            if (data.length > 0) {
                $("#selectPendiente").val(data[0].idPendiente)
                $("#selectCategoriaRecordatorio").val(data[0].idCategoria)
                $("#txtMensaje").val(data[0].mensaje)
                $("#txtFechaHora").val(data[0].fechaHora)
                $("#frmRecordatorio").data("edit-id", id)
            }
        })
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

