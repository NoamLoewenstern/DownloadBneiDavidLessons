import React from 'react';
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
        className='btn lesson-row'
        style={{ color: 'white' }}
        disabled={downloading}
        onClick={() => downloadFile(link, newFileName)}
      >
        <i className='fa fa-download'></i> הורדה
      </button>
      {downloading && (
        <>
          <i className='fa fa-refresh fa-spin' style={{ marginRight: '3px' }} />
        </>
      )}
      {/* {error && <h4>error</h4>} */}
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
    <tr className='lessons-row' key={index}>
      <th scope='row'>{index + 1}</th>
      <td>{lesson.subject}</td>

      <td style={{ verticalAlign: 'middle', whiteSpace: 'nowrap' }}>
        {lesson.rabi}
      </td>
      <td>{lesson.name}</td>
      <td>{lesson.serieName}</td>
      <td>{lesson.date}</td>
      <td style={{ verticalAlign: 'middle', whiteSpace: 'nowrap' }}>
        {lesson.length}
      </td>
      <td>
        {lesson.videoLink &&
          DownloadButton(
            lesson,
            lesson.videoLink,
            'mp4',
            downloadingVideo,
            downloadAudioVideoFile,
            errorVideo,
          )}
      </td>
      <td>
        {lesson.audioLink &&
          DownloadButton(
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
