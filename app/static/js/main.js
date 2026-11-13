
// ======================================
// JAVASCRIPT GENERAL DE VETCARE
// ======================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("VetCare: sistema cargado correctamente.");

    // Confirmación antes de eliminar registros
    const botonesEliminar = document.querySelectorAll(
        "[data-confirm-delete]"
    );

    botonesEliminar.forEach(function (boton) {

        boton.addEventListener("click", function (event) {

            const confirmar = confirm(
                "¿Estás seguro de que deseas eliminar este registro?"
            );

            if (!confirmar) {
                event.preventDefault();
            }

        });

    });

});
