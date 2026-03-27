import React from "react";
import "../css/Loader.css"; // import the external css
 
const Loader = () => {
  return (
      <div className="loader">
    <div className="loader-rings">
      <div></div>
      <div></div>
      <div></div>
      <div></div>  {/* this becomes the center dot */}
    </div>
    <div className="loader-bar">
      <span></span>
    </div>
    <p className="loader-text">Loading...</p>
  </div>
  );
};
 
export default Loader;