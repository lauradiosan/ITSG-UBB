import React from "react";
import './App.css';
import NavigationBar from './layout/NavigationBar';
import UploadImagesContainer from "./medicalImage/UploadImagesContainer";
import SignUp from "./auth/SignUp";
import SignIn from "./auth/SignIn";
import {BrowserRouter as Router, Route} from "react-router-dom";
import ImagesList from "./history/ImagesList";

function App() {
    return (
        <div className="Med3Web">
            <NavigationBar/>
            <div className={"container-fluid"}>
                <Router>
                    <switch>
                        <Route exact path="/">
                            <UploadImagesContainer/>
                        </Route>
                        <Route exact path="/SignUp">
                            <SignUp/>
                        </Route>
                        <Route exact path="/SignIn">
                            <SignIn/>
                        </Route>
                        <Route exact path="/UploadImages">
                            <UploadImagesContainer/>
                        </Route>
                        <Route path="/ImagesList">
                            <ImagesList/>
                        </Route>
                    </switch>
                </Router>
            </div>
        </div>
    );
}

export default App;
