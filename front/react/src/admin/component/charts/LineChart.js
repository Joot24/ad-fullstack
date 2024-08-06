import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Title,
    Tooltip,
    Legend
);

const LineChart = ({ data , view, labels }) => {
    const chartOptions = {
        responsive: true,
        scales: {
            'y-axis-1': {
                type: 'linear',
                position: 'left',
                display: view === 'capital',
                title: {
                    display: true,
                    text: 'Capital ($)',
                    color: '#eee',
                    font: {
                        size: 14
                    }
                },

                ticks: {
                    color: '#eee', // Tick color
                    font: {
                        size: 12
                    }
                },

                grid: {
                    color: 'grey' // Grid color
                }
            },
            'y-axis-2': {
                type: 'linear',
                position: 'left',
                display: view === 'percentChange',
                title: {
                    display: true,
                    text: 'Percent Change (%)',
                    color: '#eee', // Title color
                    font: {
                        size: 14
                    }
                },

                ticks: {
                    color: '#eee', // Tick color
                    font: {
                        size: 12
                    }
                },

                grid: {
                    color: 'grey' // Grid color
                }
            },

            x: {
                title: {
                    display: true,
                    text: `Elapsed Time (${labels[labels.length - 1]} minutes)`,
                    color: '#eee',
                    font: {
                        size: 14
                    }
                },
                ticks: {
                    color: '#eee',
                    font: {
                        size: 12
                    },
                    callback: function(value, index, values) {
                        return index === 0 || index === values.length - 1 ? this.getLabelForValue(value) : '';
                    }
                }
            },
        }

    };

    return <Line data={data} options={chartOptions} />;
};

export default LineChart;