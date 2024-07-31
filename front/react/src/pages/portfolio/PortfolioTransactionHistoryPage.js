import React from 'react';
import useTransactionHistory from '../../hooks/useTransactionHistory';
import TransactionHistoryListView from '../../components/listView/TransactionHistoryListView';

const PortfolioTransactionHistoryPage = ({ portfolioType }) => {
    const { transactions, loadMoreTransactions, hasMore } = useTransactionHistory('portfolio', portfolioType);

    return (
        <div>
            <h2>{portfolioType} Portfolio Transaction History</h2>
            <TransactionHistoryListView
                transactions={transactions}
                loadMoreTransactions={loadMoreTransactions}
                hasMore={hasMore}
            />
        </div>
    );
};

export default PortfolioTransactionHistoryPage;