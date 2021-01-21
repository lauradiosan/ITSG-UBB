import React from 'react';
import '../App.css';

class AboutUs extends React.Component {
    render() {
        return (
            <div className="intro-container">
                <h1 className="title">Our vision</h1>
                <p className="yellow-p">Nowadays we have a rather unusual situation, because of the COVID-19 pandemic. There are restric-tions everywhere we go, especially inside. And these restrictions are meant to protect the people andhinder the spread of the Corona virus. And the most problematic spaces are represented by the publicspaces that are inside, where the virus can be easily spread to the all the persons that will be presentin that room during a period of time. Even though it was recommended to practice social distancing, there are many cases where from various reasons this is not respected.Therefore, the goal of our system is to diminish the spread of Corona virus and to protect peoplefrom getting infected and spreading it further more to their close relatives and friends. At the sametime, we plan on helping all the public and private buildings that would like to keep every person thatis present in different rooms inside their building safe, by tracking every person inside a room, togetherwith the information regarding the social distancing.</p>
                <h1 className="title">What? Why? How?</h1>
                <p className="yellow-p">The year 2020 has proven to be different from many points of view, the main reason being the Covid19 pandemic that took by surprise the entire globe. People had to adapt to this peculiar virus and adopted a set of rules to fight the "invisible enemy". Among those, we find the so-called "social distancing" which basically can be translated as a safe distance maintained between two persons. This rule was supported by the World Health Organization so it quickly gained popularity among the countries. It became a standard and a thing that had to be consider in our day to day life.</p>
                <h2 className="title2">What is the (scientific) problem?</h2>
                <div className="columns">
                    <p className="yellow-p">The ordinary life we live has to address the social distancing problem now in all indoor spaces (classrooms, offices, buses, supermarkets and others). This has a huge impact on the overall society's well being. Nonetheless, this has to be monitored and maintained. To do such a thing, companies have adapted: employed people just for surveillance, to insure the distance is kept or adjusted the employment contract for some in order to add a chore to their daily list of actions.</p>
                    <p className="yellow-p">In most of the cases, this can be automated. We identified the scientific problem as to automatically identify the number of people in a space, as well as the distance between people. Moreover, provide this information in a nice manner, in a web application to the person interested, be it a manager of a space, the bus driver or the class teacher. It should be structured as a dashboard where all the details are displayed.</p>
                </div>
                <h2 className="title2">Why is it important?</h2>
                <p className="yellow-p">Finding an automated solution for this problem would mean saving a lot of time and effort from the employees in charge. It is also an actual, real problem that the society is facing, a problem of momentum. We consider that it is a perfect situation in which machine learning can improve the quality of life, maybe even help save it. </p>
                <div className="columns">
                    <div style={{ maxWidth: "500px" }}>
                        <h2 className="title2">Investigated approach</h2>
                        <p className="yellow-p">Our algorithm is composed of three main steps: capturing the image from a room, pedestrian detectionand distance approximation between pairs of pedestrian bounding boxes.</p>
                        <img style={{ maxWidth: "500px" }} src="Flow-diagram.png" alt="AlwaysRIght project Architecture"></img>
                    </div>
                    <div style={{ maxWidth: "500px" }}>
                        <h2 className="title2">People Detection</h2>
                        <p className="yellow-p">For the pedestrian detection algorithm, we have chosen to use a state of the art machine learning ap-proach, namely the third version of YOLO. This choice was mainly done because the YOLO algorithmpresents the best trade-off between accuracy and performance which is an important aspect for analyz-ing the real-time computer vision tasks. The YOLO model has several advantages over classifier-basedsystems. The novel approach that the model brings is that it looks at the whole image at test timeso its predictions are informed by global context in the image. It also makes predictions with a singlenetwork evaluation unlike systems like R-CNN which require thousands for a single image, provingthat the model is more than 1000x faster than R-CNN and 100x faster than Fast R-CNN. After somebench testing, we selected YOLOv3-tiny for our algorithm. Once the bounding boxes are detected bythe model, the next step in our algorithm is computing the distance between pedestrians in order toprovide information on the social distancing status.</p>
                        <h2 className="title2">Room monitoring system</h2>
                        <p className="yellow-p">For monitoring the room, the system consists of a Raspberry-Pi board and an auxiliary camera(Raspberry-Pi Camera v2). The Raspberry-Pi device exposes a REST API that can be used to retrieve live imagesfrom the camera. The camera is controller by using the Android Things API and takes a snapshot ofthe room whenever the client sends a GET request to the endpoint.</p>
                        <img src="schematics.jpg" alt="Room monitoring system schema" style={{ maxWidth: "500px", margin: "10px" }}></img>

                    </div>

                </div>

            </div>
        )
    }
}

export default AboutUs;