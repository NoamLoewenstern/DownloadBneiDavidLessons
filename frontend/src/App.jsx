import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import './index.css';
import './styles/App.css';
import ListLessons from './components/ListLessons';
import { listBackgroundURLs } from 'config/network';

const randomBGImageURL =
	listBackgroundURLs[Math.floor(Math.random() * listBackgroundURLs.length)];
const Appstyle = {
	// margin: '10px',
	

	backgroundImage: `url(${randomBGImageURL})`,
};
const App = () => {
	return (
		<div className="App-header" style={Appstyle}>
			<ListLessons />
		</div>
	);
};
export default App;
