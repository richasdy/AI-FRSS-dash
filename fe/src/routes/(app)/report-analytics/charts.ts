export const securityIncidentsChartData = {
    options: {
        chart: { type: "bar" as const },
        series: [
            {
                name: 'Motion Detection',
                data: [65, 59, 80, 81, 56, 40, 30],
            },
            {
                name: 'Face Recognition',
                data: [28, 48, 40, 19, 36, 27, 20],
            },
            {
                name: 'Intrusion Alert',
                data: [10, 15, 8, 12, 5, 3, 2],
            }
        ],
        xaxis: { categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] },
        legend: {
            position: 'top',
            horizontalAlign: 'center',
        },
    }
};

export const incidentsChartData = {
    options: {
        chart: { type: 'pie' as const },
        series: [35, 25, 20, 15, 5],
        labels: ['Front Gate', 'Lobby', 'Parking Lot', 'Warehouse', 'Other'],
        legend: {
            position: 'bottom',
            horizontalAlign: 'center',
        },
    }
};