import React from "react";
import "../css/Carousel.css"; // optional custom styles
import chocolate from "../image/chocolate.jpg";
import birthday from "../image/birthday.jpg";
import strawberry from "../image/strawberry.jpg";

const CarouselComponent = () => {
  return (
    <div
        id="cakeCarousel"
        className="carousel slide carousel-dark"
        data-bs-ride="carousel"
        data-bs-interval="5000"
        style={{ maxWidth: "900px", margin: "50px auto", zIndex: 2, position: "relative" }}
        >
      <div className="carousel-indicators">
        <button
          type="button"
          data-bs-target="#cakeCarousel"
          data-bs-slide-to="0"
          className="active"
          aria-current="true"
          aria-label="Slide 1"
        ></button>
        <button
          type="button"
          data-bs-target="#cakeCarousel"
          data-bs-slide-to="1"
          aria-label="Slide 2"
        ></button>
        <button
          type="button"
          data-bs-target="#cakeCarousel"
          data-bs-slide-to="2"
          aria-label="Slide 3"
        ></button>
      </div>
      <div className="carousel-inner">
        <div className="carousel-item active">
          <img
            src= {chocolate} 
            className="d-block w-100"
            alt="Chocolate Cake"
          />
          <div className="carousel-caption d-none d-md-block">
            <h5>Delicious Chocolate Cake</h5>
            <p>Rich, creamy, and perfect for any occasion.</p>
          </div>
        </div>
        <div className="carousel-item">
          <img
            src={strawberry}
            className="d-block w-100"
            alt="Strawberry Cake"
          />
          <div className="carousel-caption d-none d-md-block">
            <h5>Strawberry Delight</h5>
            <p>Fresh strawberries and cream for the perfect treat.</p>
          </div>
        </div>
        <div className="carousel-item">
          <img
            src={birthday}
            className="d-block w-100"
            alt="Birthday Cake"
          />
          <div className="carousel-caption d-none d-md-block">
            <h5>Birthday Surprise</h5>
            <p>Colorful, fun, and unforgettable cakes for every party.</p>
          </div>
        </div>
      </div>
      <button
        className="carousel-control-prev"
        type="button"
        data-bs-target="#cakeCarousel"
        data-bs-slide="prev"
      >
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button
        className="carousel-control-next"
        type="button"
        data-bs-target="#cakeCarousel"
        data-bs-slide="next"
      >
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
  );
};

export default CarouselComponent;