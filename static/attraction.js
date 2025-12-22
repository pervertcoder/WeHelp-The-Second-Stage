"use strict";

const attractionName = document.querySelector(".attractionName");
const categoryMrt = document.querySelector(".categoryMrt");

const mainDes = document.querySelector(".mainDes");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");

const clickE = document.querySelector(".clickE");
clickE.addEventListener("click", () => {
  window.location.href = "/";
});

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
};

getAttractionIdData();
