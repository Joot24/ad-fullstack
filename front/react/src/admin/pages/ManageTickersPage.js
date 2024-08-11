import React, { useState } from 'react';
import useTickers from '../hooks/useTickers';

const ManageTickersPage = () => {
    const {
        activeTickers,
        availableTickers,
        loading,
        addTicker,
        deleteTicker
    } = useTickers();

    // State to control the visibility of the Available Tickers section
    const [showAvailableTickers, setShowAvailableTickers] = useState(false);

    // Local state to keep track of selected portfolio types for each ticker
    const [selectedPortfolios, setSelectedPortfolios] = useState({});

    const handlePortfolioChange = (tickerId, portfolioType) => {
        // Update only the selected ticker's portfolio type in the state
        setSelectedPortfolios((prevSelectedPortfolios) => ({
            ...prevSelectedPortfolios,
            [tickerId]: portfolioType
        }));
    };

    const handleAddTicker = (ticker) => {
        const portfolioType = selectedPortfolios[ticker.id];

        if (!portfolioType) {
            alert("Please select a portfolio type before adding the ticker.");
            return;
        }

        // Check if the ticker with the selected portfolio already exists in the active tickers
        const tickerExists = activeTickers.some(
            activeTicker => activeTicker.id === ticker.id && activeTicker.portfolioType === portfolioType
        );

        if (tickerExists) {
            alert("This ticker with the selected portfolio is already in the active tickers list.");
        } else {
            // Add portfolioType to the ticker before adding to active tickers
            const tickerWithPortfolio = { ...ticker, portfolioType };
            addTicker(tickerWithPortfolio);

            // Optionally, clear the selected portfolio after adding the ticker
            setSelectedPortfolios((prevSelectedPortfolios) => {
                const newSelectedPortfolios = { ...prevSelectedPortfolios };
                delete newSelectedPortfolios[ticker.id];
                return newSelectedPortfolios;
            });
        }
    };

    const handleSave = () => {
        // Implement save functionality, e.g., persist changes to the server
        alert("Changes saved successfully!");
        setShowAvailableTickers(false);
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>Manage Tickers</h1>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                    <h2>Active Tickers</h2>
                    <table>
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>Ticker Name</th>
                            <th>Ticker Type</th>
                            <th>Portfolio</th>
                            <th>Action</th>
                        </tr>
                        </thead>
                        <tbody>
                        {activeTickers.map(ticker => (
                            <tr key={ticker.id}>
                                <td>{ticker.id}</td>
                                <td>{ticker.tickerName}</td>
                                <td>{ticker.tickerType}</td>
                                <td>{ticker.portfolioType}</td>
                                <td>
                                    <button onClick={() => deleteTicker(ticker.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
                <div>
                    <button onClick={() => setShowAvailableTickers(true)}>Add Ticker</button>
                    {showAvailableTickers && (
                        <div>
                            <h2>Available Tickers</h2>
                            <table>
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Ticker Name</th>
                                    <th>Ticker Type</th>
                                    <th>Portfolio</th>
                                    <th>Action</th>
                                </tr>
                                </thead>
                                <tbody>
                                {availableTickers.map(ticker => (
                                    <tr key={ticker.id}>
                                        <td>{ticker.id}</td>
                                        <td>{ticker.tickerName}</td>
                                        <td>{ticker.tickerType}</td>
                                        <td>
                                            <select
                                                value={selectedPortfolios[ticker.id] || ''}
                                                onChange={(e) => handlePortfolioChange(ticker.id, e.target.value)}
                                            >
                                                <option value="" disabled>Select</option>
                                                <option value="AGGRESSIVE">AGGRESSIVE</option>
                                                <option value="MODERATE">MODERATE</option>
                                                <option value="CONSERVATIVE">CONSERVATIVE</option>
                                            </select>
                                        </td>
                                        <td>
                                            <button onClick={() => handleAddTicker(ticker)}>Add</button>
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
            <div style={{ marginTop: '20px' }}>
                <button onClick={handleSave}>Save</button>
            </div>
        </div>
    );
};

export default ManageTickersPage;
