import { css } from "@emotion/core";
import "styles/listLessons.css";
import "styles/header.scss";
import useAxios from "axios-hooks";
import React, { useMemo } from "react";
import BeatLoader from "react-spinners/BeatLoader";
import { API_URL } from "config";
import FetchHeader from "./FetchHeader";
import LessonsTable from "./LessonsTable";
import queryString from "query-string";

// const FileDownload = require('js-file-download');

const ListLessons = props => {
  const [{ data = [], loading: fetching, error }, refetch] = useAxios(
    { method: "GET" },
    {
      manual: true
    }
  );
  const listLessons = useMemo(
    () => (Array.isArray(data) ? Array.from(data) : []),
    [data]
  );

  const handleFetch = bneiDavidFileUrl => {
    const queryArgs = queryString.stringify({ url: bneiDavidFileUrl });
    refetch({
      url: `${API_URL.fetchVideos}?${queryArgs}`
    });
  };

  return (
    <>
      <FetchHeader {...{ handleFetch, fetching }} />
      {fetching ? (
        <BeatLoader
          css={css`
            display: block;
            margin: auto 5px;
          `}
          sizeUnit={"px"}
          size={40}
          color="dodgerblue"
        />
      ) : (
        listLessons.length > 0 && <LessonsTable listLessons={listLessons} />
      )}
      {error && (
        <div className="error-msg">
          <h4>Error:</h4>
          <h5>{JSON.stringify(error.response.data)}</h5>
        </div>
      )}
    </>
  );
};

export default ListLessons;
