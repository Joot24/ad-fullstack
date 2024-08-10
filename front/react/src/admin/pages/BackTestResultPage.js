import React, {useState} from 'react';
import { useLocation } from 'react-router-dom';
import LineChart from "../component/charts/LineChart";
import '../../assets/styles/BackTestResultPage.css'
import Button from "../../components/common/buttons/Button";
import Heading from "../../components/common/text/Heading";
import CardComponent from "../../components/common/cards/CardWithChart";

const BackTestResultPage = () => {
    const location = useLocation();
    const { labels, datasets } = location.state;
    const [view, setView] = useState('capital');

    // toggle between different views
    const handleToggle = () => {
        setView(view === 'capital' ? 'percentChange' : 'capital');
    };

    function formatLabels(labels) {
        return labels.map(label => {
            const [year, month, day, hour, minute] = label;
            const date = new Date(year, month - 1, day, hour, minute);

            // Options for the formatting
            const options = {
                year: 'numeric',
                month: 'short',  // 'short' for abbreviated month name, 'long' for full name
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true, // true for 12-hour time, false for 24-hour time
            };

            return date.toLocaleString('en-SG', options); // Adjust format as needed
        });
    }
    const formattedLabels = formatLabels(labels);

    const data = {
        labels: formattedLabels,
        datasets: view === 'capital' ? [
                {
                    label: 'Capital',
                    data: datasets[0].data,
                    yAxisID: 'y-axis-1',
                    borderColor: '#800000',
                    backgroundColor: '#800000',
                    tension: 0.4,
                }] :
            [
                {
                    label: 'Percent Change',
                    data: datasets[1].data,
                    yAxisID: 'y-axis-2',
                    borderColor: '#000080',
                    backgroundColor: '#000080',
                    tension: 0.4,
                },
            ],
    };

    return (
        <div>
            <CardComponent
                title={<Heading as="h1" size="lg" color="brand.600" mb={2}>BackTest Performance</Heading>}
                chart={<LineChart data={data} view={view} labels={labels}/>}
                button={<Button color="brand.600" onClick={handleToggle}>
                    Toggle View
                </Button>}
            />
        </div>
    );
};

export default BackTestResultPage;
