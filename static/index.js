"use strict";

// banner 101 image
// const image101 = document.querySelector(".image101");
const putImage101 = async function () {
  const url = "/api/attractions?page=0&keyword=101";
  const req = await fetch(url);

  const response = await req.json();
  const data = response.data[0];
  const bannerImage = data.image[0];
  console.log(bannerImage);

  image101.src = bannerImage;
};

// putImage101();
