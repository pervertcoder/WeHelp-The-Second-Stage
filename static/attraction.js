"use strict";

const getAttractionIdData = async function () {
  const hRef = window.location.href;
  const hRefAr = hRef.split("/");
  const id = hRefAr[4];
  //   console.log(id);

  let url = `/api/attraction/${id}`;
  const res = await fetch(url);
  const data = await res.json();
  console.log(data);
};

getAttractionIdData();
