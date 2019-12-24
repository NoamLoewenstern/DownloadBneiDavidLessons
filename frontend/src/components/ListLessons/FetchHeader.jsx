import React, { useState, useEffect } from 'react';
import useLocalStorage from 'react-use-localstorage';
import { mainPage } from 'config';
import validUrl from 'valid-url';
const FetchHeader = ({ handleFetch, fetching }) => {
  const [urlLocalStorage, setUrlLocalStorage] = useLocalStorage('url', '');
  const [url, setUrl] = useState(urlLocalStorage);

  useEffect(() => {
    handleFetch(urlLocalStorage || mainPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const isValidUrl = url => {
    let errMsg = '';
    if (!url) {
      errMsg = `כתובת ריקה`;
    } else if (!validUrl.isWebUri(url)) {
      errMsg = `'${url}' כתובת לא הגיונית`;
    }
    if (errMsg) {
      alert(errMsg);
      return false;
    }
    return true;
  };

  const handleOnClickShowLessons = () => {
    if (isValidUrl(url)) {
      setUrlLocalStorage(url);
      handleFetch(url);
    }
  };

  const handleOnClickCurrentUrl = async () => {
    if (!isValidUrl(url)) return false;
    setUrlLocalStorage(url);
    window.open(url, '_blank');
  };

  return (
    <div className='fetch-header'>
      <h2>
        הורדת שיעורים מאתר{' '}
        <a
          href='http://www.bneidavid.org/Web/He/VirtualTorah/Lessons/Default.aspx'
          rel='noopener noreferrer'
          target='_blank'
        >
          בני דוד
        </a>
      </h2>
      <div>
        <input
          type='text'
          value={url}
          required
          onChange={e => setUrl(e.target.value)}
          placeholder='URL'
          onKeyDown={e => e.key === 'Enter' && handleOnClickShowLessons()}
        />
        <button onClick={handleOnClickShowLessons} disabled={fetching}>
          הצג שיעורים
        </button>
        {url && (
          <button
            className='current-url'
            href={url}
            rel='noopener noreferrer'
            target='_blank'
            onClick={handleOnClickCurrentUrl}
          >
            פתח נוכחי
          </button>
        )}
      </div>
    </div>
  );
};

export default FetchHeader;
