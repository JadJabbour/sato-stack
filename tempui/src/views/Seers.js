import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react plugin used to create charts
import { Line, Bar } from "react-chartjs-2";

import { useState } from "react";
import { useEffect } from "react";

// reactstrap components
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  Label,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
  UncontrolledTooltip,
} from "reactstrap";

function Seers(props) {
  const [bigChartData, setbigChartData] = React.useState("data1");
  const setBgChartData = (name) => {
    setbigChartData(name);
  };

  const [selectedTicker, setSelectedTicker] = useState("BTC");
  const [historicalData, setHistoricalData] = useState({});
  const [historicalDataReal, setHistoricalDataReal] = useState({});

  useEffect(() => {
    fetch("http://167.71.60.98:9000/ticker?ticker=" + selectedTicker)
      .then((response) => response.json())
      .then((responseJson) => {
        setHistoricalData(responseJson);

        fetch(
          "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" +
            selectedTicker +
            "&market=USD&apikey=O20KZP2GSD1YCDQG&outputsize=full"
        )
          .then((response) => response.json())
          .then((responseJson) => {
            setHistoricalDataReal(
              responseJson["Time Series (Digital Currency Daily)"]
            );
          });
      });
  }, [selectedTicker]);

  function getValues(type) {
    var array = [];
    Object.keys(historicalData).map((item, i) => {
      array.push(Object.values(Object.values(historicalData)[i])[type]);
    });

    return array;
  }

  function getValuesReal(type) {
    var strType = "test";

    switch (type) {
      case 0:
        strType = "1a. open (USD)";
        break;
      case 1:
        strType = "2a. high (USD)";
        break;
      case 2:
        strType = "3a. low (USD)";
        break;
      case 3:
        strType = "4a. close (USD)";
        break;
      default:
        strType = "1a. open (USD)";
    }

    var array = [];
    Object.keys(historicalData).map((item, i) => {
      var idx = JSON.stringify(Object.keys(historicalData)[i].split(" ")[0]);
      idx = idx.replace('"', "").replace('"', "");

      if (
        historicalDataReal[idx] != null &&
        historicalDataReal[idx][strType] != null
      ) {
        array.push(historicalDataReal[idx][strType]);
      }
    });

    return array;
  }

  function testClick(t) {
    if (t.target.value.length >= 3) setSelectedTicker(t.target.value);
  }

  return (
    <>
      <div className="content">
        <Row>
          <Col xs="1"></Col>
          <Col xs="10">
            <label>
              <h4 className="ticker-label"> Change Ticker </h4>
            </label>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <select
              onChange={(t) => testClick(t)}>
              <option value="BTC">BTC</option>
              <option value="ETH">ETH</option>
              <option value="SOL">SOL</option>
              <option value="ADA">ADA</option>
            </select>
            <span> [SOL, ADA, ETH, BTC... more soon] </span>
          </Col>
        </Row>

        <Row>
          <Col xs="1"></Col>
          <Col xs="10">
            <Card className="card-chart">
              <CardHeader>
                <Row>
                  <Col className="text-left" sm="6">
                    <CardTitle tag="h2">{selectedTicker} Closed</CardTitle>
                  </Col>
                </Row>
              </CardHeader>
              <CardBody>
                <Line
                  data={{
                    labels: Object.keys(historicalData),
                    datasets: [
                      {
                        label: "Close",
                        data: getValues(0),
                        fill: false,
                        backgroundColor: "#1f8ef1",
                        borderColor: "#1f8ef1",
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        pointBackgroundColor: "#1f8ef1",
                        pointBorderColor: "rgba(255,255,255,0)",
                        pointHoverBackgroundColor: "#1f8ef1",
                        pointBorderWidth: 20,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 15,
                        pointRadius: 4,
                      },
                      {
                        label: "Real Close",
                        data: getValuesReal(0),
                        fill: false,
                        backgroundColor: "#1f8e50",
                        borderColor: "#1f8e50",
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        pointBackgroundColor: "#1f8e50",
                        pointBorderColor: "rgba(255,255,255,0)",
                        pointHoverBackgroundColor: "#1f8e50",
                        pointBorderWidth: 20,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 15,
                        pointRadius: 4,
                      },
                    ],
                  }}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Seers;
