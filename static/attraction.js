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

const radioAll = document.getElementsByName("time");
console.log(radioAll);
const price = document.querySelector(".priceS");
if (radioAll[0].checked) {
  price.textContent = "新台幣2000元";
}
if (radioAll[1].checked) {
  price.textContent = "新台幣2500元";
} else {
  price.textContent = "新台幣";
}

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
