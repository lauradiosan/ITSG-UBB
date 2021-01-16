import React from "react";
import { Bar, Line } from "react-chartjs-2";
import { useLocation } from "react-router-dom";

let dataFromTable = [];

function Statistics() {
  let location = useLocation();

  //nr of persons will be in -> location.state.rooms[0].num_persons);
  //current date will be in -> location.state.currentDate);

  let employeesPerMonth = [100, 592, 801, 81, 156, 269, 444, 59, 255, 653, 123];
  let employeesPerDay = []
  let totalSum = 0;
  if (location.state !== undefined) {
    dataFromTable[location.state.currentDate.getHours()] =
      location.state.rooms[0].num_persons;

    let roomsDetails = location.state.rooms;
    for (let i = 0; i < roomsDetails.length; i++) {
      if (i < location.state.currentDate.getHours() - 9) {
        employeesPerDay.push(parseInt(roomsDetails[i].num_persons));
      }
      totalSum += parseInt(roomsDetails[i].num_persons);
    }
    employeesPerMonth.push(totalSum);
  } else {
    for (let i = 0; i < (new Date()).getHours() - 9; i++) {
      employeesPerDay.push(i + 10);
    }
    employeesPerMonth.push(100);
  }

  var state_line_chart = {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December"
    ],
    datasets: [
      {
        label: "Employees Density",
        labelColor: "blue",
        fill: true,
        lineTension: 0.5,
        backgroundColor: "#B0E0E6",
        borderColor: "black",
        hoverBorderColor: "blue",
        fontColor: "white",
        borderWidth: 2,
        data: employeesPerMonth,
      },
    ],
  };

  var state_bar_chart = {
    labels: [
      "10:00",
      "11:00",
      "12:00",
      "13:00",
      "14:00",
      "15:00",
      "16:00",
      "17:00",
      "18:00",
    ],
    datasets: [
      {
        label: "Employees Density",
        fontColor: "#FFF",
        fill: true,
        lineTension: 0.5,
        backgroundColor: "#3f8efc",
        borderColor: "black",
        hoverBorderColor: "white",
        borderWidth: 2,
        data: employeesPerDay,
      },
    ],
  };

  return (
    <div className="intro-container" style={{ padding: "20px" }}>
      <h1 className="title">Statistics on the density of people</h1>
      <Bar
        data={state_bar_chart}
        options={{
          title: {
            display: true,
            text: "Average number of employees per hour",
            fontSize: 30,
            fontColor: "#0a2463",
          },
          legend: {
            display: true,
            position: "right",
            labels: {
              fontColor: "#0a2463",
              fontSize: 20,
            },
          },
          tooltips: {
            bodyFontColor: "green",
            footerFontColor: "green",
            fontSize: 40,
          },
          scales: {
            yAxes: [
              {
                ticks: {
                  fontColor: "#3f8efc",
                  fontSize: 20,
                  beginAtZero: true,
                },
              },
            ],
            xAxes: [
              {
                ticks: {
                  fontColor: "#3f8efc",
                  fontSize: 20,
                  beginAtZero: true,
                },
              },
            ],
          },
        }}
      />
      <Line
        data={state_line_chart}
        options={{
          responsive: true,
          title: {
            display: true,
            text: "Number of employees per month",
            fontSize: 30,
            fontColor: "#0a2463",
          },
          legend: {
            display: true,
            position: "right",
            labels: {
              fontColor: "#0a2463",
              fontSize: 20,
            },
          },
          scales: {
            yAxes: [
              {
                ticks: {
                  fontColor: "#3f8efc",
                  fontSize: 20,
                  beginAtZero: true,
                },
              },
            ],
            xAxes: [
              {
                ticks: {
                  fontColor: "#3f8efc",
                  fontSize: 20,
                  beginAtZero: true,
                },
              },
            ],
          },
        }}
      />
    </div>
  );
}

export default Statistics;
