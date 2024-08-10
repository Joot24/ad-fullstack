import React from 'react';
import { useParams } from 'react-router-dom';
import PortfolioAddFunds from "../../components/portfolio/PortfolioAddFunds";
import PortfolioWithdrawFunds from "../../components/portfolio/PortfolioWithdrawFunds";
import Heading from "../../components/common/text/Heading";
import usePortfolio from "../../hooks/usePortfolio";
import PortfolioDetails from "../../components/portfolio/PortfolioDetails";
import portfolioTypes from "./portfolioTypes";
import RulesPageModal from "../../pages/portfolio/rules/RulesPageModal";
import {Box, Center} from "@chakra-ui/react";

const PortfolioManager = () => {
    const { portfolioType } = useParams();
    const { portfolio, addFunds, withdrawFunds } = usePortfolio(portfolioType.toUpperCase());

    const selectedPortfolioType = portfolioTypes.find(pt => pt.type.toLowerCase() === portfolioType);
    const title = selectedPortfolioType ? selectedPortfolioType.title : 'Portfolio';

    return (
        <Center>
            <Box>
                <Heading>{title}</Heading>
                <PortfolioDetails portfolio={portfolio}/>
                <PortfolioAddFunds addFunds={addFunds}/>
                <PortfolioWithdrawFunds withdrawFunds={withdrawFunds} currentBalance={portfolio.allocatedBalance}/>
                {/*todo: to remove - RulesPage replaced by RulesPageModal*/}
                {/*<button onClick={handleNavigateToRules}>Rules page</button>*/}
                {/* Manage Rules Modal Button */}
                <RulesPageModal triggerText="Manage Rules"
                                modalTitle={title}
                                portfolioType={portfolioType.toUpperCase()}/>
            </Box>
        </Center>
    );
};

export default PortfolioManager;
