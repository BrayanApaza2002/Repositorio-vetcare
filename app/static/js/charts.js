
document.addEventListener("DOMContentLoaded", function () {

    // Obtener datos enviados desde Flask
    const elementoCitas = document.getElementById("graficoCitas");
    const elementoEspecies = document.getElementById("graficoEspecies");
    const elementoIngresos = document.getElementById("graficoIngresos");

    // Gráfico de citas por estado
    if (elementoCitas) {
        new Chart(elementoCitas, {
            type: "doughnut",
            data: {
                labels: JSON.parse(elementoCitas.dataset.labels),
                datasets: [{
                    label: "Cantidad de citas",
                    data: JSON.parse(elementoCitas.dataset.values),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

    // Gráfico de mascotas por especie
    if (elementoEspecies) {
        new Chart(elementoEspecies, {
            type: "bar",
            data: {
                labels: JSON.parse(elementoEspecies.dataset.labels),
                datasets: [{
                    label: "Cantidad de mascotas",
                    data: JSON.parse(elementoEspecies.dataset.values),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    // Gráfico de ingresos mensuales
    if (elementoIngresos) {
        new Chart(elementoIngresos, {
            type: "line",
            data: {
                labels: JSON.parse(elementoIngresos.dataset.labels),
                datasets: [{
                    label: "Ingresos (Bs)",
                    data: JSON.parse(elementoIngresos.dataset.values),
                    tension: 0.3,
                    fill: true,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

});
