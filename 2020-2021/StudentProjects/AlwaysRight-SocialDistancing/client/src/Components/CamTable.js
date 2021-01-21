import axios from "axios";
import React from "react";
import Lightbox from "react-image-lightbox";
import "react-image-lightbox/style.css"; // This only needs to be imported once in your app
import { Link } from "react-router-dom";
import ReactTable from "react-table";
import "react-table/react-table.css";
import "../App.css";

class CamTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rooms: [
        {
          num_persons: "120",
          room_name: "Room Omega",
          id: "1",
          image: null,
        },
      ],
      isFeedOpen: false,
      currentFeedImage: null,
      currentDate: new Date(),
    };
    this.recheck = this.recheck.bind(this);
    this.view_feed = this.view_feed.bind(this);
  }

  componentDidMount() {
    axios.get("http://localhost:1331/predict").then((res) => {
      this.setState({ rooms: res.data["rooms"], currentDate: new Date() });
    });
  }

  findPositionById(roomId) {
    return this.state.rooms.findIndex((x) => x.id === roomId);
  }

  recheck(roomId) {
    const pos = this.findPositionById(roomId);
    axios.get("http://localhost:1331/predict_room/" + roomId).then((res) => {
      this.setState((oldState) => {
        let rooms = oldState.rooms.slice();
        let copy = Object.assign({}, rooms[pos]);
        copy.num_persons = res.data.num_persons;
        copy.image = res.data.image;
        rooms[pos] = copy;
        return {
          rooms: rooms,
        };
      });
    });
  }

  view_feed(room_id) {
    const pos = this.findPositionById(room_id);
    const image = this.state.rooms[pos].image;
    let content = "data:image/jpeg;base64," + image;
    this.setState({ isFeedOpen: true, currentFeedImage: content });
  }

  render() {
    let roomNames = ["Alpha", "Theta", "Gamma", "Beta", "Zeta", "Eta", "Epsilon", "Peta"];
    const columns = [
      {
        Header: "Room Id",
        accessor: "id",
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Room Name",
        accessor: "room_name",
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Number of Persons",
        accessor: "num_persons",
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Action",
        Cell: (props) => {
          return (
            <button
              type="button"
              className="tableButton"
              onClick={() => {
                this.recheck(props.original.id);
              }}
            >
              Update
            </button>
          );
        },
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Live Feed",
        Cell: (props) => {
          return (
            <button
              type="button"
              className="tableButton"
              onClick={() => {
                this.view_feed(props.original.id);
              }}
            >
              View
            </button>
          );
        },
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Statistics",
        Cell: (props) => {
          return (<button
            type="button"
            className="tableButton">
            <Link style={{ color: "white" }}
              to={{
                pathname: "/statistics",
                state: this.state,
              }}
            >
              Statistics
          </Link>
          </button>);
        },
        style: {
          textAlign: "center",
        },
      }
    ];

    for (let i = parseInt(this.state.rooms[this.state.rooms.length - 1].id, 10) + 1; i <= 8; i++) {
      let name = roomNames[Math.floor(Math.random() * roomNames.length)];
      var index = roomNames.indexOf(name)
      this.state.rooms.push({
        num_persons: Math.floor(Math.random() * 200).toString(),
        room_name: "Room " + name,
        id: i.toString(),
        image: null,
      });
      roomNames.splice(index, 1);
    }
    const data = this.state.rooms;
    const isFeedOpen = this.state.isFeedOpen;
    const currentFeedImage = this.state.currentFeedImage;
    return (
      <div>
        <ReactTable
          className="tableStyle"
          columns={columns}
          data={data}
          showPagination={false}
          defaultPageSize={this.state.rooms.length}
        ></ReactTable>
        {isFeedOpen && currentFeedImage != null && (
          <Lightbox
            mainSrc={currentFeedImage}
            onCloseRequest={() => this.setState({ isFeedOpen: false })}
          ></Lightbox>
        )}
      </div>
    );
  }
}

export default CamTable;
