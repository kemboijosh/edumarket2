function Getproducts() {
  return (
    <div className="container mt-4">
      <h2>Welcome to EduMarket</h2>

      <div id="carouselExample" className="carousel slide mt-3">
        <div className="carousel-inner">

          <div className="carousel-item active">
            <img src="https://via.placeholder.com/800x300" className="d-block w-100" alt=""/>
            <div className="carousel-caption">
              <h5>Buy Quality Products</h5>
            </div>
          </div>

          <div className="carousel-item">
            <img src="https://via.placeholder.com/800x300" className="d-block w-100" alt=""/>
            <div className="carousel-caption">
              <h5>Best Prices Available</h5>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}

export default Getproducts;