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
    price.textContent = "新台幣 2000 元";
  }
  if (radioAll[1].checked) {
    price.textContent = "新台幣 2500 元";
  }
};
for (let i = 0; i < radioAll.length; i++) {
  radioAll[i].addEventListener("change", () => {
    priceChanged();
  });
}

// API獲取+畫面渲染
const imgSlider = document.querySelector(".imgSlider");
const arrowRight = document.getElementById("nextBtn");
const arrowLeft = document.getElementById("prevBtn");
const indicators = document.getElementById("indicators");
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

  // 圖片
  const imgArr = attraction.image;
  imgSlider.src = imgArr[0];

  // 指示器
  const imgArrLen = imgArr.length;
  for (let i = 0; i < imgArrLen; i++) {
    const sonIndi = document.createElement("div");
    sonIndi.setAttribute("class", "sonIndi");
    sonIndi.dataset.id = i;

    indicators.appendChild(sonIndi);
  }

  const sons = document.querySelectorAll(".sonIndi");
  const coloredSon0 = Array.from(sons).filter((son) => son.dataset.id === "0");
  coloredSon0[0].classList.add("sonIndi__stat--on");

  // 輪播
  let currentPos = 0;
  const lengthAr = imgArr.length;

  arrowRight.addEventListener("click", () => {
    if (currentPos < lengthAr - 1) {
      imgSlider.src = imgArr[currentPos + 1];
      currentPos += 1;
      const coloredSons = Array.from(sons).filter(
        (son) =>
          son.dataset.id === String(currentPos) ||
          son.dataset.id === String(currentPos - 1)
      );
      coloredSons[0].classList.remove("sonIndi__stat--on");
      coloredSons[1].classList.add("sonIndi__stat--on");
    }
    if (currentPos === lengthAr - 1) {
      console.log("no more data");
    }
  });

  arrowLeft.addEventListener("click", () => {
    if (currentPos !== 0) {
      imgSlider.src = imgArr[currentPos - 1];
      currentPos -= 1;
      const coloredSons = Array.from(sons).filter(
        (son) =>
          son.dataset.id === String(currentPos) ||
          son.dataset.id === String(currentPos + 1)
      );
      coloredSons[0].classList.add("sonIndi__stat--on");
      coloredSons[1].classList.remove("sonIndi__stat--on");
    } else {
      console.log("no more image");
    }
  });
};

getAttractionIdData();
