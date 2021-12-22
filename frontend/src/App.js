import React from 'react';
import './App.css';
import routes from './routes';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import MenuApp from './components/Menu/MenuApp';

function App() {
  const showContentRoutes = (routes) => {
    let results = [];
    if(routes.length > 0) {
      results = routes.map((route, index) => {
        return <Route key={index} exact={route.exact} path={route.path} component={route.main} />
      });
    };
    return results;
  };

  return (
    <Router>
      <MenuApp />
      <div className="App">
        <Switch>
          {showContentRoutes(routes)}
        </Switch>
      </div>
    </Router>
  );
}

export default App;
