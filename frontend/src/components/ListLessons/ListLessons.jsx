import 'styles/ListLessons/table.scss';
import 'styles/header.scss';
import useAxios from 'axios-hooks';
import React, { useMemo, useCallback } from 'react';
import BeatLoader from 'react-spinners/BeatLoader';
import useLocalStorage from 'react-use-localstorage';
import { mainPage } from 'config';

import FetchHeader from './FetchHeader';
import LessonsTable from './LessonsTable';
import { getAPIReqEncodedUrl, genErrorMsg } from './helpers';

const ListLessons = props => {
  const [urlLocalStorage, setUrlLocalStorage] = useLocalStorage('url', '');
  const [{ data = [], loading: fetching, error }, fetch] = useAxios(
    getAPIReqEncodedUrl(urlLocalStorage || mainPage),
  );

  const listLessons = useMemo(
    () => (Array.isArray(data) ? Array.from(data) : []),
    [data],
  );

  const handleFetch = useCallback(
    bneiDavidFileUrl => {
      const apiReqUrl = getAPIReqEncodedUrl(bneiDavidFileUrl);
      setUrlLocalStorage(bneiDavidFileUrl);
      fetch(apiReqUrl);
    },
    [fetch, setUrlLocalStorage],
  );

  return (
    <>
      <FetchHeader {...{ handleFetch, fetching }} />
      {fetching ? (
        <BeatLoader sizeUnit={'px'} size={40} color='dodgerblue' />
      ) : (
        listLessons.length > 0 && <LessonsTable listLessons={listLessons} />
      )}
      {genErrorMsg(error)}
    </>
  );
};

export default ListLessons;
