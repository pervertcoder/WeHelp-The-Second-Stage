"use strict";

const attractionName = document.querySelector(".attractionName");
const categoryMrt = document.querySelector(".categoryMrt");

const mainDes = document.querySelector(".mainDes");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");

// 首頁連結
const clickE = document.querySelector(".clickE");
clickE.addEventListener("click", () => {
  window.location.href = "/";
});

// 價錢依據時段改變
const radioAll = document.getElementsByName("time");
const price = document.querySelector(".priceS");
const priceChanged = function () {
  if (radioAll[0].checked) {
    price.textContent = "新台幣2000元";
  }
  if (radioAll[1].checked) {
    price.textContent = "新台幣2500元";
  }
};
for (let i = 0; i < radioAll.length; i++) {
  radioAll[i].addEventListener("change", () => {
    priceChanged();
  });
}

// API獲取+畫面渲染
const imgSlider = document.querySelector(".imgSlider");
const getAttractionIdData = async function () {
  const hRef = window.location.href;
  const hRefAr = hRef.split("/");
  const id = hRefAr[4];

  let url = `/api/attraction/${id}`;
  const res = await fetch(url);
  const data = await res.json();
  const attraction = data.data;
  console.log(attraction);

  attractionName.textContent = attraction.name;
  categoryMrt.textContent = `${attraction.category} at ${attraction.mrt}`;

  mainDes.textContent = attraction.description;
  address.textContent = attraction.address;
  transport.textContent = attraction.transport;

  const imgArr = attraction.image;
  imgSlider.src = imgArr[0];
};

getAttractionIdData();

// 圖片輪播函式
const arrowRight = document.getElementById("nextBtn");
const arrowLeft = document.getElementById("prevBtn");

const getImgSlider = async function () {
  const hRef = window.location.href;
  const hRefAr = hRef.split("/");
  const id = hRefAr[4];

  let url = `/api/attraction/${id}`;
  const res = await fetch(url);
  const data = await res.json();
  const attraction = data.data;
  const imgArr = attraction.image;
  return imgArr;
};

const sliderChanged = async function () {
  const imgArr = await getImgSlider();
  let currentPos = 0;
  const lengthAr = imgArr.length;

  arrowRight.addEventListener("click", () => {
    if (currentPos < lengthAr - 1) {
      imgSlider.src = imgArr[currentPos + 1];
      currentPos += 1;
    }
    if (currentPos === lengthAr - 1) {
      console.log("no more data");
    }
  });

  arrowLeft.addEventListener("click", () => {
    if (currentPos !== 0) {
      imgSlider.src = imgArr[currentPos - 1];
      currentPos -= 1;
    } else {
      console.log("no more image");
    }
  });
};

sliderChanged();
