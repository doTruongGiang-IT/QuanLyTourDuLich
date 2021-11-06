import TourDetailsPage from "./pages/TourDetails/TourDetailsPage";
import TourListPage from "./pages/TourListPage/TourListPage";
import AddTourPage from "./pages/AddTourPage/AddTourPage";
import GuestsPage from "./pages/GuestsPage/GuestsPage";
import TourFactorPage from "./pages/TourFactorsPage/TourFactorsPage";

const routes = [
    {
        exact: true,
        path: '/',
        main: () => <TourListPage />
    }, 
    {
        exact: true,
        path: '/add',
        main: () => <AddTourPage />
    }, 
    {
        exact: true,
        path: '/details/:id',
        main: () => <TourDetailsPage />
    }, 
    {
        exact: true,
        path: '/guests/:id',
        main: () => <GuestsPage />
    }, 
    {
        exact: true,
        path: '/tour_factors',
        main: () => <TourFactorPage />
    }
];

export default routes;