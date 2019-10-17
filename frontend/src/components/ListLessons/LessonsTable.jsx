import React from 'react';
import LessonRow from './LessonRow';
import { Table } from 'react-bootstrap';

const LessonHeader = () => {
	return (
		<tr>
			<th>#</th>
			<th>נושא</th>
			<th>הרב</th>
			<th>שיעור</th>
			<th>סדרה</th>
			<th>תאריך</th>
			<th>אורך</th>
			<th>סרטון</th>
			<th>שמע</th>
		</tr>
	);
};

const LessonsTable = ({ listLessons }) => {
	return (
		<Table striped bordered hover variant="dark">
			<thead>
				<LessonHeader />
			</thead>
			<tbody>
				{listLessons.map((lesson, index) => (
					<LessonRow lesson={lesson} key={index} index={index} />
				))}
			</tbody>
		</Table>
	);
};

export default LessonsTable;
