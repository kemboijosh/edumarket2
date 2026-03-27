import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./component/Navbar";
import Footer from "./component/Footer";
import Signin from "./component/Signin";
import Signup from "./component/Signup";
import Addproducts from "./component/Addproducts";
import Getproducts from "./component/Getproducts";
import Makepayment from "./component/Makepayment";
import Aboutus from "./component/Aboutus";
import Contact from "./component/Contact";
import Notfound from "./component/Notfound";

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route path="/" element={<Getproducts />} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/add" element={<Addproducts />} />
        <Route path="/pay" element={<Makepayment />} />
        <Route path="/about" element={<Aboutus />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<Notfound />} />
      </Routes>

      <Footer />
    </Router>
  );
}

export default App;