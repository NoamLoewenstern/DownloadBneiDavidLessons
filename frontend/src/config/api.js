export const localBackendURL =
  !process.env.NODE_ENV || process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    : "";
export const API_URL = {
  fetchVideos: localBackendURL + "/fetch",
  downloadFile: localBackendURL + "/downloadFile",
  backgroundImage: localBackendURL + "/backgroundImage"
};
