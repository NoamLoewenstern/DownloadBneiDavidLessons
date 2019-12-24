import 'styles/ListLessons/table.scss';
import 'styles/header.scss';
import useAxios from 'axios-hooks';
import React, { useMemo, Fragment } from 'react';
import BeatLoader from 'react-spinners/BeatLoader';
import { API_URL } from 'config';
import FetchHeader from './FetchHeader';
import LessonsTable from './LessonsTable';
import queryString from 'query-string';

const ListLessons = props => {
  const [{ data = [], loading: fetching, error }, refetch] = useAxios(
    { method: 'GET' },
    {
      manual: true,
    },
  );
  const listLessons = useMemo(
    () => (Array.isArray(data) ? Array.from(data) : []),
    [data],
  );

  const handleFetch = bneiDavidFileUrl => {
    const queryArgs = queryString.stringify({ url: bneiDavidFileUrl });
    refetch({
      url: `${API_URL.fetchVideos}?${queryArgs}`,
    });
  };
  console.log({ error });
  const errorMsg = () => {
    const { response, message: errMessage } = error || {};
    const { status, statusText, data: errData } = response || {};
    const innerErrMsg =
      status === 500 &&
      statusText === 'INTERNAL SERVER ERROR' &&
      errData.startsWith('<!DOCTYPE')
        ? errData
        : (errData && JSON.stringify(errData)) || errMessage || '';
    return (
      error && (
        <>
          <h4>שגיאה:</h4>
          <div
            className='error-msg'
            style={{ backgroundColor: '#2d2d2d' }}
            dangerouslySetInnerHTML={{ __html: innerErrMsg }}
          />
        </>
      )
    );
  };

  return (
    <>
      <FetchHeader {...{ handleFetch, fetching }} />
      {fetching ? (
        <BeatLoader sizeUnit={'px'} size={40} color='dodgerblue' />
      ) : (
        listLessons.length > 0 && <LessonsTable listLessons={listLessons} />
      )}
      {errorMsg() || ''}
    </>
  );
};

export default ListLessons;
