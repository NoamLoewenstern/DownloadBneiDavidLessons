export const BASE_BNEI_URL = "http://www.bneidavid.org";
export const listBackgroundURLs = [
  "/Items/05889/001.jpg",
  "/Items/05890/002.jpg",
  "/Items/05891/003.jpg",
  "/Items/00427/004.jpg",
  "/Items/00426/005.jpg",
  "/Items/00428/006.jpg",
  "/Items/00429/007.jpg"
].map(picPath => BASE_BNEI_URL + picPath);

export const mainPage =
  BASE_BNEI_URL + "/Web/He/VirtualTorah/Lessons/Default.aspx";
export const dbgUrl =
  mainPage + "?subject=&rabi=&name=%d7%a7%d7%a6%d7%a8&subjectText=&rabiText=";
