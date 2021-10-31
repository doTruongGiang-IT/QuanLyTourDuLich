import TourDetailsPage from "./pages/TourDetails/TourDetailsPage";
import TourListPage from "./pages/TourListPage/TourListPage";
import AddTourPage from "./pages/AddTourPage/AddTourPage";
import GuestsPage from "./pages/GuestsPage/GuestsPage";

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
    }
];

export default routes;