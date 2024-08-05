import React from "react";
import { Route } from "react-router-dom";
import PortfolioPage from "../pages/portfolio/PortfolioPage";
import ConservativePage from "../pages/portfolio/ConservativePage";
import ModeratePage from "../pages/portfolio/ModeratePage";
import AggressivePage from "../pages/portfolio/AggressivePage";

const portfolioRoutes = [
    <Route key="portfolio" path="/portfolio" element={<PortfolioPage />} />,
    <Route key="conservative" path="/portfolio/conservative" element={<ConservativePage />} />,
    <Route key="moderate" path="/portfolio/moderate" element={<ModeratePage />} />,
    <Route key="aggressive" path="/portfolio/aggressive" element={<AggressivePage />} />
];

export default portfolioRoutes;

