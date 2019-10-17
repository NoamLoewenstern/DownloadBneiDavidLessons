import React, { useState, useEffect } from "react";
import { mainPage } from "config";

const FetchHeader = ({ handleFetch, fetching }) => {
  const [url, setUrl] = useState("");

  // dbg
  useEffect(() => {
    // setUrl(mainPage);
    handleFetch(mainPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="fetch-header">
      <h2>הורד שיעורים מאתר "בני דוד"</h2>
      <div>
        <input
          type="text"
          value={url}
          required
          onChange={e => setUrl(e.target.value)}
          placeholder="URL"
        />
        <button onClick={() => handleFetch(url)} disabled={fetching}>
          הצג שיעורים
        </button>
      </div>
    </div>
  );
};

export default FetchHeader;
