import React from 'react';

const AvailableTickerItem = ({ ticker, onAdd }) => {
    return (
        <div>
            <span>{ticker.tickerType}: {ticker.tickerName}</span>
            <button onClick={() => onAdd(ticker)}>Add</button>
        </div>
    );
};

export default AvailableTickerItem;