import 'styles/ListLessons/table.scss';
import 'styles/header.scss';
import useAxios from 'axios-hooks';
import React, { useMemo, useCallback } from 'react';
import BeatLoader from 'react-spinners/BeatLoader';
import useLocalStorage from 'react-use-localstorage';

import { API_URL } from 'config';
import FetchHeader from './FetchHeader';
import LessonsTable from './LessonsTable';
import queryString from 'query-string';

const ListLessons = props => {
  const [urlLocalStorage, setUrlLocalStorage] = useLocalStorage('url', '');

  const [{ data = [], loading: fetching, error }, fetch] = useAxios(
    { method: 'GET', url: urlLocalStorage },
    {
      manual: false,
    },
  );
  const listLessons = useMemo(
    () => (Array.isArray(data) ? Array.from(data) : []),
    [data],
  );

  const handleFetch = useCallback(
    bneiDavidFileUrl => {
      const queryArgs = queryString.stringify({ url: bneiDavidFileUrl });
      console.log(`calling 'fetch' on ${bneiDavidFileUrl}`);
      setUrlLocalStorage(urlLocalStorage);
      fetch({
        url: `${API_URL.fetchVideos}?${queryArgs}`,
      });
    },
    [fetch, urlLocalStorage, setUrlLocalStorage],
  );
  const errorMsg = '';
  // useMemo(() => {
  //   if (!error) return '';
  //   const { response, message: errMessage } = error || {};
  //   const { status, statusText, data: errData } = response || {};
  //   const innerErrMsg =
  //     status === 500 &&
  //     statusText === 'INTERNAL SERVER ERROR' &&
  //     typeof errData === 'string' &&
  //     errData.startsWith('<!DOCTYPE')
  //       ? errData
  //       : (errData && JSON.stringify(errData)) || errMessage || '';
  //   return (
  //     error && (
  //       <>
  //         <h4>שגיאה:</h4>
  //         <div
  //           className='error-msg'
  //           style={{ backgroundColor: '#2d2d2d' }}
  //           dangerouslySetInnerHTML={{ __html: innerErrMsg }}
  //         />
  //       </>
  //     )
  //   );
  // }, [error]);

  return (
    <>
      <FetchHeader {...{ handleFetch, fetching }} />
      {fetching ? (
        <BeatLoader sizeUnit={'px'} size={40} color='dodgerblue' />
      ) : (
        listLessons.length > 0 && <LessonsTable listLessons={listLessons} />
      )}
      {errorMsg}
    </>
  );
};

export default ListLessons;
