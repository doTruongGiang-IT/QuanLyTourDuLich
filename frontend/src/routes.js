import TourDetailsPage from "./pages/TourDetails/TourDetailsPage";
import TourListPage from "./pages/TourListPage/TourListPage";
import AddTourPage from "./pages/AddTourPage/AddTourPage";
import GuestsPage from "./pages/GuestsPage/GuestsPage";
import TourFactorPage from "./pages/TourFactorsPage/TourFactorsPage";
import AddGroupPage from "./pages/AddGroupPage/AddGroupPage";
import UpdateGroupPage from "./pages/UpdateGroupPage/UpdateGroupPage";
import CustomerPage from "./pages/CustomerPage/CustomerPage";
import CreateCustomerPage from "./pages/CreateCustomerPage/CreateCustomerPage";
import StatsPage from "./pages/StatsPage/StatsPage";

const routes = [
    {
        exact: true,
        path: '/',
        main: () => <TourListPage />
    }, 
    {
        exact: true,
        path: '/customer',
        main: () => <CustomerPage />
    }, 
    {
        exact: true,
        path: '/stats',
        main: () => <StatsPage />
    }, 
    {
        exact: true,
        path: '/create_customer',
        main: () => <CreateCustomerPage />
    }, 
    {
        exact: true,
        path: '/add',
        main: () => <AddTourPage />
    }, 
    {
        exact: true,
        path: '/add/groupTour/:id',
        main: () => <AddGroupPage />
    }, 
    {
        exact: true,
        path: '/update/groupTour/:id',
        main: () => <UpdateGroupPage />
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