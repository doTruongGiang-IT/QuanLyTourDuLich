import TourDetailsPage from "./pages/TourDetails/TourDetailsPage";
import TourListPage from "./pages/TourListPage/TourListPage";
import AddTourPage from "./pages/AddTourPage/AddTourPage";

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
    }
];

export default routes;