import React, { useState, useEffect } from 'react';
import { ProgressButton } from 'react-progress-button';
// import styled from 'styled-components';
import { useDownloadBneiDavidFile } from 'components/custom';

const DownloadButton = (
	lesson,
	link,
	ext,
	downloading,
	downloadFile,
	error,
) => {
	const newFileName = `${lesson.rabi} - ${lesson.name}.${ext}`;
	return (
		<>
			<button
				class="btn lesson-row"
				style={{ color: 'white' }}
				disabled={downloading}
				onClick={() => downloadFile(link, newFileName)}>
				<i class="fa fa-download"></i> הורדה
			</button>
			{downloading && (
				<>
					<i className="fa fa-refresh fa-spin" style={{ marginRight: '3px' }} />
				</>
			)}
			{error && <h4>error</h4>}
		</>
	);
};

const LessonRow = ({ lesson, index }) => {
	const [
		{ downloading: downloadingVideo, errorVideo },
		downloadAudioVideoFile,
	] = useDownloadBneiDavidFile();
	const [
		{ downloading: downloadingAudio, errorAudio },
		downloadAudioFile,
	] = useDownloadBneiDavidFile();

	return (
		<tr className="lessons-row" key={index}>
			<th style={{ verticalAlign: 'middle' }} scope="row">
				{index + 1}
			</th>
			<td style={{ verticalAlign: 'middle' }}>{lesson.subject}</td>

			<td style={{ verticalAlign: 'middle', whiteSpace: 'nowrap' }}>
				{lesson.rabi}
			</td>
			<td style={{ verticalAlign: 'middle' }}>{lesson.name}</td>
			<td style={{ verticalAlign: 'middle' }}>{lesson.serieName}</td>
			<td style={{ verticalAlign: 'middle' }}>{lesson.date}</td>
			<td style={{ verticalAlign: 'middle', whiteSpace: 'nowrap' }}>
				{lesson.length}
			</td>
			<td style={{ verticalAlign: 'middle' }}>
				{/* <a href={lesson.videoLink}>Video</a> */}
				{DownloadButton(
					lesson,
					lesson.videoLink,
					'mp4',
					downloadingVideo,
					downloadAudioVideoFile,
					errorVideo,
				)}
			</td>
			<td style={{ verticalAlign: 'middle' }}>
				{/* <a href={lesson.audioLink}>Audio</a> */}
				{DownloadButton(
					lesson,
					lesson.audioLink,
					'mp3',
					downloadingAudio,
					downloadAudioFile,
					errorAudio,
				)}
			</td>
		</tr>
	);
};

export default LessonRow;
