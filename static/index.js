"use strict";

const attractionContent = document.querySelector(".attraction__content");

// 生成DOM
const renderAttractions = function (data) {
  // const fragment = document.createDocumentFragment();

  for (let i = 0; i < data.length; i++) {
    const attractionContentUnit = document.createElement("div");
    const imageShell = document.createElement("div");
    const attractionImage = document.createElement("img");
    const attractionInfo = document.createElement("div");
    const attractionInfoText = document.createElement("p");
    const attractionData = document.createElement("div");
    const attractionDataRight = document.createElement("p");
    const attractionDataLeft = document.createElement("p");

    attractionContentUnit.setAttribute("class", "attraction__content--unit");
    imageShell.setAttribute("class", "imageShell");
    attractionImage.setAttribute("class", "aImage");
    attractionInfo.setAttribute("class", "attractionInfo");
    attractionData.setAttribute("class", "attractionData");
    attractionDataRight.setAttribute("class", "attractionDataRight");
    attractionDataLeft.setAttribute("class", "attractionDataLeft");

    attractionContent.appendChild(attractionContentUnit);
    attractionContentUnit.appendChild(imageShell);
    imageShell.appendChild(attractionImage);
    imageShell.appendChild(attractionInfo);
    attractionInfo.appendChild(attractionInfoText);
    attractionContentUnit.appendChild(attractionData);
    attractionData.appendChild(attractionDataLeft);
    attractionData.appendChild(attractionDataRight);

    attractionImage.src = data[i].image[0];
    attractionInfoText.textContent = data[i].name;
    attractionDataLeft.textContent = data[i].mrt;
    attractionDataRight.textContent = data[i].category;

    // fragment.appendChild(attractionContentUnit);
  }

  // attractionContent.appendChild(fragment);
};

// 抓取景點資料，並回傳下一頁的頁數
const getAttractionData = async function (
  url = "/api/attractions?page=",
  page = 0,
  qur = "",
  keyword = ""
) {
  let finalUrl = url + page + qur + keyword;
  const req = await fetch(finalUrl);
  const response = await req.json();
  const data = response.data;
  const pageField = response.nextPage;
  // console.log(pageField);

  renderAttractions(data);
  return pageField;
};

// 讀取下一頁資料的函式
const sentinel = document.querySelector("#scrollSentinel");
let currentPage = 1;
let isLoading = false;

const loadNextPage = async function () {
  if (isLoading) return;
  isLoading = true;

  let url = "/api/attractions?page=";
  let nextPage = await getAttractionData(url, currentPage);
  if (nextPage !== null) {
    currentPage = nextPage;
  } else {
    observer.unobserve(sentinel);
    console.log("已經沒有更多資料");
  }

  isLoading = false;
};

// 建立intersection observer
const observer = new IntersectionObserver(
  async (entries) => {
    const entry = entries[0];
    if (entry.isIntersecting) {
      loadNextPage();
    }
  },
  {
    root: null,
    rootMargin: "0px",
    threshold: 0.9,
  }
);

// 畫面生成
async function init(
  url = "/api/attractions?page=",
  page = 0,
  qur = "",
  keyword = ""
) {
  attractionContent.innerHTML = "";
  await getAttractionData();

  requestAnimationFrame(() => {
    observer.observe(sentinel);
  });
}

init();

// 生成DOM
const categoryAlign = function (data) {
  for (let i = 0; i < data.length; i++) {
    const filterRoom = document.createElement("div");
    const filterBtn = document.createElement("button");

    filterRoom.classList.add("filter__room");
    filterBtn.classList.add("filter__button");
    filterBtn.classList.add(`filter__button${i}`);
    filterBtn.type = "button";

    filterCategory.appendChild(filterRoom);
    filterRoom.appendChild(filterBtn);

    filterBtn.textContent = data[i];
  }
};

// 獲取API資料
const filterCategory = document.querySelector(".filter__category--structure");

const getCategory = async function () {
  let url = "/api/categories";
  const req = await fetch(url);

  const response = await req.json();
  let categoryData = response.data;
  console.log(categoryData);

  let newCategoryData = ["全部分類"];
  for (const i of categoryData) {
    newCategoryData.push(i);
  }
  // console.log(newCategoryData);

  categoryAlign(newCategoryData);
};

getCategory();

// 顯示開關
const allCategory = document.querySelector(".filter__btn");
const filterPanel = document.querySelector(".filter__category--structure");

let stat = false;
const pointer = function () {
  if (!stat) {
    filterPanel.classList.remove("filter__state--off");
    filterPanel.classList.add("filter__state--on");
    stat = true;
  }
};
allCategory.addEventListener("click", pointer);

filterPanel.addEventListener("click", (e) => {
  if (e.target.classList.contains("filter__button")) {
    const text = e.target.textContent;

    switch (text) {
      case "全部分類":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "養生溫泉":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "藍色公路":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "歷史建築":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "藝文館所":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "單車遊蹤":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "戶外踏青":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "宗教信仰":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "其他":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "親子共遊":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
    }
  }
});

// 篩選搜尋事件
const search = document.getElementById("search");
const searchWord = document.getElementById("filter__ip").value;
const searchCategory = document.querySelector(".filter__btn").textContent;
let urll = "/api/attractions?page=";
let pagge = 0;

search.addEventListener("click", () => {
  init(urll, pagge, "&category=" + searchCategory, "&keyword=" + searchWord);
});
