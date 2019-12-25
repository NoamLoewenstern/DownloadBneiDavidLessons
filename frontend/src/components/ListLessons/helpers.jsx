import React from 'react';
import { API_URL } from 'config';
import queryString from 'query-string';

export const getAPIReqEncodedUrl = bneiDavidFileUrl => {
  const queryArgs = queryString.stringify({ url: bneiDavidFileUrl });
  return `${API_URL.fetchVideos}?${queryArgs}`;
};

export const genErrorMsg = error => {
  if (!error) return '';
  const { response, message: errMessage } = error || {};
  const { status, statusText, data: errData } = response || {};
  const innerErrMsg =
    status === 500 &&
    statusText === 'INTERNAL SERVER ERROR' &&
    typeof errData === 'string' &&
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
