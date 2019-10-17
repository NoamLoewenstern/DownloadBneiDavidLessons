import { useState, useEffect, useRef } from 'react';
import useAxios from 'axios-hooks';
import randomstring from 'randomstring';
import { API_URL } from 'config';
import { jsonify } from 'utils';
import queryString from 'query-string';

const useDownloadBneiDavidFile = (config = {}, options = {}, fname = '') => {
	const [{ data = null, loading: downloading, error }, fetchFile] = useAxios(
		{ method: 'GET', ...config },
		{
			manual: true,
			...options,
		},
	);
	const [filename, setFilename] = useState(
		fname ||
			randomstring.generate({
				length: 5,
				charset: 'alphabetic',
			}),
	);
	const downloadFile = async (bneiDavidFileUrl, filename) => {
		filename && setFilename(filename);
		const queryArgs = queryString.stringify({ url: bneiDavidFileUrl });
		fetchFile({
			url: `${API_URL.downloadFile}?${queryArgs}`,
			responseType: 'blob',
		});
	};
	const linkRef = useRef(document.createElement('a'));

	useEffect(() => {
		document.body.appendChild(linkRef.current);
	}, []);

	useEffect(() => {
		linkRef.current.setAttribute('download', filename);
	}, [filename]);

	useEffect(() => {
		if (data) {
			let resp;
			if ((resp = jsonify(data)) && resp.status === 'Error') {
				console.error(resp);
				return;
			}
			const url = window.URL.createObjectURL(new Blob([data]));
			linkRef.current.href = url;
			linkRef.current.click();
		}
	}, [data]);

	return [{ downloading, error }, downloadFile];
};

export { useDownloadBneiDavidFile };
