import React from "react";
import logo from "../logo.svg";
import "./NavigationBar.css";
import AuthService from "../auth/AuthService";

const authService = AuthService();

const NavigationBar = () => {

    const isLoggedIn = authService.isLoggedIn();
    let username = authService.loggedUser();

    const logout = async () => {
        try {
            const response = await authService.signOut();
            window.open("/", "_self");
        }
        catch (e) {
            //todo
        }
    }

    const goToHomePage = () => {
        window.open("/UploadImages", "_self");
    }

    const goToImageHistoryPage = () => {
        window.open("/ImagesList", "_self");
    }

    return (
        <div className={"Navigation-bar"}>
            <img src={logo} className="App-logo NavItem" alt="logo" onClick={goToHomePage}/>
            <div className="NavItem" onClick={goToHomePage}>
                Social Good Team
            </div>
            {
                isLoggedIn
                ?
                <div className={"float-right h4"}> 
                    <label className={"m-2 text-decoration-none text-muted highlightOver"}>Hi, {username}!</label>
                    <button className={"m-2 btn-primary"} onClick={goToImageHistoryPage}>Image history</button>
                    <button onClick={logout} className={"m-2 btn-danger"}>Logout</button>
                </div>
                :
                <div className={"float-right h4"}>
                    <a href="SignUp" className={"m-2 text-decoration-none text-muted highlightOver"}>Sign Up</a>
                    <a href="SignIn" className={"m-2 text-decoration-none text-muted highlightOver"}>Sign In</a>
                </div>
            }
        </div>
    );
}

export default NavigationBar;