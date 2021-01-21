import React from 'react';
import '../App.css';
import { Player } from 'video-react';
import "../../node_modules/video-react/dist/video-react.css";
import OurVideo from "../assets/our-movie.mov"

class PageIntro extends React.Component {
    state = {
        videoFileURL: OurVideo,
        videoFileObject: null
    }

    render() {
        return (
            <div className="intro-container">
                <h1 className="title">Automated System for Social Density</h1>
                <Player
                    playsInline
                    src={this.state.videoFileURL}
                />
                <h2 className="title2" style={{ marginTop: "10%" }}>Members</h2>
                <p className="members-p">Berciu Liviu</p>
                <p className="members-p">Cotrau Andreea</p>
                <p className="members-p">Tamas Florin</p>
                <p className="members-p">Ungur Maria</p>
            </div >
        )
    }
}

export default PageIntro;