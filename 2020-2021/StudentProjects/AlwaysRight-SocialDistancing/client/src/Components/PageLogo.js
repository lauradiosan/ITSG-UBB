import React from 'react';
import { ReactComponent as Logo } from '../alwaysrightfin.svg';
import '../App.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

class PageLogo extends React.Component {
    render() {
        return <header>
            <Navbar bg="#95D7AE" expand="lg">
                <Navbar.Brand href="/"><Logo className="logo-container" /></Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link href="/"><span className="link-btn">Home</span></Nav.Link>
                        <Nav.Link href="#camtable"><span className="link-btn">Surveillance</span></Nav.Link>
                        <Nav.Link href="#aboutus"><span className="link-btn">About Us</span></Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </header>;
    }
}

export default PageLogo;