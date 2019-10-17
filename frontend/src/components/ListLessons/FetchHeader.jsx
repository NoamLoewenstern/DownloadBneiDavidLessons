import React, { useState, useEffect } from 'react';
import { mainPage } from 'config';
import validUrl from 'valid-url';

const FetchHeader = ({ handleFetch, fetching }) => {
  const [url, setUrl] = useState('');

  useEffect(() => {
    handleFetch(mainPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const handleOnClickCurrentUrl = async () => {
    if (validUrl.isUri(url)) {
      window.open(url, '_blank');
    } else {
      alert(`'${url}' כתובת לא קיימת`);
    }
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
        />
        <button onClick={() => handleFetch(url)} disabled={fetching}>
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
            נוכחי
          </button>
        )}
      </div>
    </div>
  );
};

export default FetchHeader;
