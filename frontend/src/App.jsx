import "bootstrap/dist/css/bootstrap.min.css";
import React from "react";
import "./index.css";
import "./styles/App.css";
import ListLessons from "./components/ListLessons";
// import { listBackgroundURLs } from "config/network";
import { API_URL } from "config";

// const randomBGImageURL =
// 	listBackgroundURLs[Math.floor(Math.random() * listBackgroundURLs.length)];
const Appstyle = {
  // margin: '10px',
  backgroundImage: `url(${API_URL.backgroundImage})`
};
const App = () => {
  return (
    <div className="App-header" style={Appstyle}>
      <ListLessons />
    </div>
  );
};
export default App;
