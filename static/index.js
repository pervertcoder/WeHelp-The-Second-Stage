"use strict";

const attractionContent = document.querySelector(".attraction__content");

const getAttractionData = async function () {
  let url = "/api/attractions?page=0";
  const req = await fetch(url);
  const response = await req.json();
  const data = response.data;
  const pageField = response.nextPage;
  console.log(data);

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
  }
};

getAttractionData();
