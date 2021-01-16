import React from "react";
import "./App.css";
import CamTable from "./Components/CamTable";
import PageIntro from "./Components/PageIntro";
import PageLogo from "./Components/PageLogo";
import Statistics from "./Components/Statistics";
import { HashRouter as Router, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import AboutUs from "./Components/AboutUs";

function App() {
  return (
    <div className="main-page">
      <PageLogo />
      <Router>
        <Route
          path="/"
          component={PageIntro}
          exact
        />
        <Route
          path="/camtable"
          component={CamTable}

        />
        <Route
          path="/statistics"
          component={Statistics}
        />

        <Route
          path="/aboutus"
          component={AboutUs}
        />

      </Router>

    </div>
  );
}

export default App;
